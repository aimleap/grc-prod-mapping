"""
Promo Processor Module

This module provides functionality for processing promotional deals and coupons.
It includes pattern matching, deal calculations, and store brand identification.
"""

# Import required modules
import re
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Dict, Any, TypeVar, Union, List, Callable, Tuple
from pathlib import Path
from abc import ABC, abstractmethod
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import threading

# Type variables for type hinting
T = TypeVar("T", bound="PromoProcessor")  # Type variable bound to PromoProcessor class
CONSTRUCTEUR = TypeVar("b9c49dae")  # Custom type variable for construction

# Configure basic logging with timestamp, logger name, level and message
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Create logs directory if it doesn't exist in parent directory
logs_dir = Path(__file__).resolve().parent.parent / "logs"
if logs_dir.exists():
    # Remove all files in the logs directory
        for file in logs_dir.glob('*'):
            try:
                file.unlink()
            except Exception as e:
                logging.error(f"Failed to remove file {file}: {str(e)}")
else:
    logs_dir.mkdir(parents=True, exist_ok=True)

# Set up rotating file handler for logging with size limit and backup count
handler = RotatingFileHandler(logs_dir / 'app.log', maxBytes=9000000, backupCount=10)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logging.getLogger().addHandler(handler)

class PromoProcessor(ABC):
    """
    Abstract base class for processing promotional deals and coupons.

    This class provides the framework for processing different types of promotional
    offers and maintaining a registry of processor implementations.
    """

    # Class-level storage for processor implementations and thread safety
    subclasses = {}  # Registry for processor subclasses
    results = []     # Storage for processing results
    _lock = threading.Lock()  # Thread lock for synchronization
    site_patterns = {}

    # Dictionary mapping number words to their integer values
    NUMBER_MAPPING = {"ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5,
                     "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10}

    # Dictionary mapping retailers to their store brand names
    marianos = ['Private Selection', 'Simple Truth', 'Kroger', 'Banner Brand', 'Smart Way', 'Abound', 'Bakery Fresh Goodness', 'Bloom Haus', 'Comforts', 'Dip', 'Everyday Living', 'HD Designs', 'Hemisfares', 'Home Chef', 'Kroger Mercado', 'Luvsome', 'Murray"s Cheese', 'Office Works', 'Pet Pride']
    Target = ['Deal Worthy', 'Good & Gather', 'Everspring', 'Favorite Day', 'Kindfull', 'Market Pantry', 'Made By Design', 'Smartly', 'Up & UP', 'Spritz', 'Figmint', 'Made by Design']
    Jewel = ['Overjoyed', 'O Organics', 'Signature Select', 'Open Nature', 'Lucerne', 'Waterfront Bistro', 'Primo Taglio', 'Value Corner', 'Soleil', 'Ready Meals', 'Debi Lilly Designs']
    Walmart = ['Great Value', 'Equate', 'Better Goods', 'Sam"s Choice', "Ol'Roy", "Special Kitty", "Clear American", "Fire Side Gourmet", "Home Bake Value", "Marketside", "Mash-up Coffee", "Spring Valley", "World Table", "Tasty", "Parent's Choice"]
    _store_brands = {
        'marianos': frozenset(marianos),
        'target': frozenset(Target),
        'jewel': frozenset(Jewel),
        'walmart': frozenset(Walmart)
    }
    # _store_brands = {
    #     'marianos': frozenset(["Private Selection", "Kroger", "Simple Truth", "Simple Truth Organic"]),
    #     'target': frozenset(["Deal Worthy", "Good & Gather", "Market Pantry", "Favorite Day", "Kindfull", "Smartly", "Up & Up"]),
    #     'jewel': frozenset(['Lucerne', "Signature Select", "O Organics", "Open Nature", "Waterfront Bistro", "Primo Taglio",
    #                 "Soleil", "Value Corner", "Ready Meals"]),
    #     'walmart': frozenset(["Clear American", "Great Value", "Home Bake Value", "Marketside",
    #                 "Co Squared", "Best Occasions", "Mash-Up Coffee", "World Table"])
    # }

    # Cache for compiled regex patterns and pre-processors
    _compiled_patterns = {}  # Cache to store compiled regex patterns
    _pre_processors = []     # List of pre-processing functions

    def __init_subclass__(cls, version='v1', **kwargs):
        """Register new implementations in the subclasses registry with version control."""
        super().__init_subclass__(**kwargs)
        if not version in cls.subclasses: cls.subclasses[version] = []
        PromoProcessor.subclasses[version].append(cls)

    def __init__(self) -> None:
        """Initialize the processor instance with class-specific logging."""
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)


    @classmethod
    def apply(cls, func: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]) -> T:
        """Apply a transformation function to the processing results."""
        cls.results = func(cls.results)
        return cls

    @classmethod
    def pre_process(cls, func: Callable[[List[Dict[str, Any]]], List[Dict[str, Any]]]) -> T:
        """Register a pre-processing function to be applied before main processing."""
        cls._pre_processors.append(func)
        return cls

    def update_save(self):
        """Save all registered patterns to a JSON file for persistence."""
        with open("patterns.json", "w") as f:
            patterns = [pattern for section in self.subclasses.values()
                       for processor_class in section
                       for pattern in processor_class().patterns]
            json.dump(patterns, f, indent=4)

    @classmethod
    @lru_cache(maxsize=1024)
    def apply_store_brands(cls, product_title: str) -> str:
        """
        Check if a product title matches any known store brands.

        Args:
            product_title: The title of the product to check

        Returns:
            'yes' if it's a store brand, 'no' otherwise
        """
        title_lower = product_title.casefold()
        for brands in cls._store_brands.values():
            if any(brand.casefold() in title_lower for brand in brands):
                return "yes"
        return "no"

    @property
    @abstractmethod
    def patterns(self):
        """Abstract property that must return the patterns for matching deals and coupons."""
        pass

    @abstractmethod
    def calculate_deal(self, item_data: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        """Abstract method to calculate deal pricing based on matched patterns."""
        pass

    @abstractmethod
    def calculate_coupon(self, item_data: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        """Abstract method to calculate coupon discounts based on matched patterns."""
        pass

    @classmethod
    def process_item(cls, item_data: Dict[str, Any]) -> T:
        """
        Process a single item or list of items with deals and coupons.
        Handles both single items and batch processing with thread pooling.

        Args:
            item_data: Dictionary containing item information or list of such dictionaries

        Returns:
            The processor instance for method chaining
        """
        # Apply any registered pre-processors
        print("***********************")
        print("when we started process_item: count is")
        print(len(item_data))
        print("***********************")

        if cls._pre_processors:
            for pre_processor in cls._pre_processors:
                print(pre_processor)
                item_data = pre_processor(item_data)
        print("***********************")
        print("when we completed pre_processor: count is")
        print(len(item_data))
        print("***********************")
        # Handle batch processing with thread pool
        if isinstance(item_data, list):
            with ThreadPoolExecutor() as executor:
                processed_items = list(executor.map(cls.process_single_item, item_data))
            with cls._lock:
                cls.results.extend(processed_items)
        else:
            # Process single item
            processed_item = cls.process_single_item(item_data)
            with cls._lock:
                cls.results.append(processed_item)
        print("***********************")
        print("when we started process_item: count is")
        print(len(item_data))
        print("***********************")

        return cls

    @classmethod
    def to_json(cls, filename: Union[str, Path]) -> None:
        """
        Save processing results to a JSON file with proper directory creation.

        Args:
            filename: Path or string for the output JSON file
        """
        if not isinstance(filename, Path):
            filename = Path(filename)
        filename = filename.with_suffix(".json") if not filename.suffix else filename
        filename.parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as f:
            json.dump(cls.results, f, indent=4)

    @classmethod
    def _get_compiled_pattern(cls, pattern: str) -> re.Pattern:
        """
        Get or create a compiled regex pattern from cache.

        Args:
            pattern: Regular expression pattern string

        Returns:
            Compiled regex pattern object
        """
        # Check if pattern is not already compiled and cached
        if pattern not in cls._compiled_patterns:
            # Compile pattern with case-insensitive flag and store in cache
            cls._compiled_patterns[pattern] = re.compile(pattern, re.IGNORECASE)
        # Return compiled pattern from cache
        return cls._compiled_patterns[pattern]

    @classmethod
    def find_best_match(cls, description: str) -> Tuple[str, re.Match, "PromoProcessor", int]:
        """
        Find the best matching pattern for a description across all processor versions.

        Args:
            description: The text to match against patterns

        Returns:
            Tuple of (pattern, match object, processor instance, score)
        """
        section_best_matches = []

        # Find best match from each version section
        for section, processor_classes in cls.subclasses.items():
            # Initialize variables to track best match in current section
            best_score = -1
            best_pattern = None
            best_match = None
            best_processor = None

            # Check each processor class in the section
            for processor_class in processor_classes:
                # Create instance of processor class
                processor = processor_class()
                # Check each pattern defined in the processor
                for pattern in processor.patterns:
                    # Get or create compiled regex pattern
                    compiled_pattern = cls._get_compiled_pattern(pattern)
                    # Try to find match in description text
                    match = compiled_pattern.search(description)
                    if match:
                        # Calculate precedence score for this pattern
                        score = cls.calculate_pattern_precedence(pattern)
                        # Update best match if current score is higher
                        if score > best_score:
                            best_score = score
                            best_pattern = pattern
                            best_match = match
                            best_processor = processor

            # If found a match in this section, add to list of best matches
            if best_pattern:
                section_best_matches.append((best_pattern, best_match, best_processor, best_score))

        # Return the overall best match based on highest score across all sections
        if section_best_matches:
            return max(section_best_matches, key=lambda x: x[3])

        # Return default values if no matches found
        return None, None, None, -1

    @classmethod
    def process_single_item(cls, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a single item's deals and coupons comprehensively.

        Args:
            item_data: Dictionary containing item information

        Returns:
            Updated item data with processed deals and coupons
        """
        # Create a copy to avoid modifying original data
        updated_item = item_data.copy()
        # Initialize logger if not already present
        if not hasattr(cls, "logger"):
            cls.logger = logging.getLogger(cls.__name__)
        # Get UPC from item data, default to empty string if not found
        upc = updated_item.get("upc", "")
        # Initialize remarks field
        updated_item["remarks"] = ""

        # Process volume deals if present in item data
        deals_desc = updated_item.get("volume_deals_description", "")
        if deals_desc:
            # Find matching pattern and processor for the deals description
            pattern, match, processor, score = cls.find_best_match(deals_desc)
            if processor and match:
                cls.site_patterns.update(
                    {f'{item_data["upc"]}.deal': {
                        "pattern": pattern,
                        "processor": f"{processor.__module__}.{processor.__class__.__name__}",
                        "score": score,
                        "promo": updated_item["volume_deals_description"]
                        }})

                # Log successful match for volume deals
                cls.logger.info(f"UPC: {upc}: DEALS: {processor.__class__.__name__}: {deals_desc}")
                # Process the deal using matched processor
                updated_item = processor.calculate_deal(updated_item, match)
                # Define filter function to check if sale price equals unit price
                filt = lambda x: x.get("sale_price") == x.get("unit_price")
                # If sale price equals unit price, clear volume deals price
                if updated_item and filt(updated_item):
                    updated_item["volume_deals_price"] = ""
                    updated_item["volume_deals_description"] = "" # newly added
                    updated_item["unit_price"] = "" # newly added
                    updated_item["remarks"] = "Volume deals has been applied to this item as sale price."

        # Return empty dict if processing failed
        if not updated_item: return {}

        # Process digital coupons if present in item data
        coupon_desc = updated_item.get("digital_coupon_description", "")
        if coupon_desc:
            # Find matching pattern and processor for the coupon description
            pattern, match, processor, score = cls.find_best_match(coupon_desc)
            if processor and match:
                cls.site_patterns.update(
                    {f'{item_data["upc"]}.coupon': {
                        "pattern": pattern,
                        "processor": f"{processor.__module__}.{processor.__class__.__name__}",
                        "score": score,
                        "promo": updated_item["digital_coupon_description"]
                        }})
                # Log successful match for digital coupons
                cls.logger.info(f"UPC: {upc}: COUPONS: {processor.__class__.__name__}: {coupon_desc}")
                # Process the coupon using matched processor
                updated_item = processor.calculate_coupon(updated_item, match)

        # Add store brand flag based on product title analysis
        updated_item["store_brand"] = cls.apply_store_brands(updated_item["product_title"])
        return updated_item

    @staticmethod
    @lru_cache(maxsize=1024)
    def calculate_pattern_precedence(pattern: str) -> int:
        """
        Calculate a score for pattern matching precedence.
        Higher scores indicate more specific patterns that should take precedence.

        Args:
            pattern: The regex pattern to score

        Returns:
            Integer score for the pattern
        """
        score = len(pattern) * 2  # Base score from pattern length
        score += len(re.findall(r'\((?!\?:).*?\)', pattern)) * 15  # Capturing groups weight
        score -= len(re.findall(r'[\*\+\?]', pattern)) * 8  # Wildcards penalty
        score -= len(re.findall(r'\{.*?\}', pattern)) * 6  # Quantifiers penalty
        score -= len(re.findall(r'\.', pattern)) * 4  # Dot wildcards penalty
        score += len(re.findall(r'\[.*?\]', pattern)) * 5  # Character classes bonus
        score += len(re.findall(r'\b', pattern)) * 3  # Word boundaries bonus
        score += len(re.findall(r'\^|\$', pattern)) * 4  # Start/end anchors bonus
        score += len(re.findall(r'\(\?:.*?\)', pattern)) * 8  # Non-capturing groups bonus
        return score

    @classmethod
    def matcher(cls, description: str) -> str:
        """
        Find the best matching pattern for a description.
        Wrapper method for find_best_match that returns only the pattern.

        Args:
            description: The text to match against patterns

        Returns:
            The best matching pattern or None
        """
        pattern, match, processor, score = cls.find_best_match(description)
        return pattern

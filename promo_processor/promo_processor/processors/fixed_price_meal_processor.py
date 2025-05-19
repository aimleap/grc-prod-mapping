from promo_processor.processor import PromoProcessor
from typing import Dict, Any
import re

class BasicFixedPriceProcessor(PromoProcessor, version=5):
    patterns = [
        r'^\$(?P<price>\d+\.?\d*)$',
        r'^\$(?P<price>\d+\.?\d*)\s+price\s',
        r'^(?P<price>\d+)¢',
    ]

    def calculate_deal(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        item_data = item.copy()
        price = float(match.group('price'))

        if "¢" in item_data["volume_deals_description"]:
            price = float(match.group('price')) / 100

        item_data["volume_deals_price"] = round(price, 2)
        item_data["unit_price"] = round(price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["required_quantity"] = 1
        item_data["limit"] = 0

        return item_data

    def calculate_coupon(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        item_data = item.copy()
        price = float(match.group('price'))
        if "¢" in item_data["digital_coupon_description"]:
            price = float(match.group('price')) / 100

        item_data["digital_coupon_price"] = round(price, 2)
        item_data["unit_price"] = round(price, 2)
        item_data["required_quantity"] = 1
        item_data["limit"] = 0

        return item_data

class LimitedFixedPriceProcessor(PromoProcessor, version=2):
    patterns = [
        r'^\$(?P<price>\d+\.?\d*)\s+When\s+Buy\s+(?P<quantity>\d+)\s+Limit\s+(?P<limit>\d+)',
    ]

    def calculate_deal(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        item_data = item.copy()
        price = float(match.group('price'))
        quantity = int(match.group('quantity'))

        item_data["volume_deals_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        item_data["required_quantity"] = quantity
        item_data["limit"] = int(match.group('limit'))

        return item_data

    def calculate_coupon(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        item_data = item.copy()
        price = float(match.group('price'))
        quantity = int(match.group('quantity'))

        item_data["digital_coupon_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["required_quantity"] = quantity
        item_data["limit"] = int(match.group('limit'))

        return item_data

class MultiQuantityFixedPriceProcessor(PromoProcessor, version=3):
    patterns = [
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)\s+or\s+more',
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+Mix\s*&\s*Match\s+multiples\s+of\s+(?P<min_quantity>\d+)',
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)',
        r'^.*(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)',
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+must\s+buy\s+(?P<min_quantity>\d+)\s+or\s+more',
    ]

    def calculate_deal(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        item_data = item.copy()
        price = float(match.group('price'))
        quantity = int(match.group('quantity'))
        min_quantity = int(match.group('min_quantity'))

        if min_quantity > quantity:
            quantity = min_quantity

        item_data["volume_deals_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        item_data["required_quantity"] = quantity
        item_data["limit"] = 0

        return item_data

    def calculate_coupon(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:
        item_data = item.copy()
        price = float(match.group('price'))
        quantity = int(match.group('quantity'))
        min_quantity = int(match.group('min_quantity'))

        if min_quantity > quantity:
            quantity = min_quantity

        item_data["digital_coupon_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["required_quantity"] = quantity
        item_data["limit"] = 0

        return item_data

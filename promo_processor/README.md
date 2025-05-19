
# Grocery Store Data Processor

A Python tool for processing promotional data from various grocery stores (Jewel-Osco, Marianos, Target).

## Features

- Processes data from multiple file formats (JSON, CSV, Excel)
- Handles promotional data including:
  - Digital coupons
  - Volume deals
  - Unit pricing
  - Regular and sale prices
- Standardizes data format across different stores
- Removes invalid promotions
- Handles multiple promotions per item
- Calculates lowest unit prices
- Formats zero values appropriately

## Usage
```bash
python main.py -f <input_file> -o <output_directory> -s <site>
```

### Arguments

- `-f, --file`: Input file path (supports .json, .csv, .xls, .xlsx)
- `-o, --output`: Output directory for processed data (defaults to output/)
- `-s, --site`: Store name (choices: jewel, marianos, target)

## File Structure

- `main.py`: Main entry point and data loading logic
- `marianos.py`: Marianos-specific data processing
- `jewelosco.py`: Jewel-Osco-specific data processing
- `target.py`: Target-specific data processing
- `promo_processor.py`: Core promotional data processing logic

## Data Processing Steps

1. Load and validate input file
2. Pre-process promotional data
3. Split multiple promotions
4. Remove invalid promotions
5. Reorder data fields
6. Skip invalid price combinations
7. Calculate lowest unit prices
8. Format zero values
9. Export processed data

## Output Format

Processed data is saved as JSON with standardized fields including:
- Store information
- Product details
- Pricing information
- Promotional data
- UPC codes
- Crawl dates

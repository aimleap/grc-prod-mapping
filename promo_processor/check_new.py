from pathlib import Path
import pandas as pd
import json
import re
import argparse


def load_file(file_path):
    file = Path(file_path)
    if not file.exists():
        raise FileNotFoundError(f"File {file} not found")
    if file.suffix == ".json":
        df = pd.read_json(file)
    elif file.suffix == ".csv":
        df = pd.read_csv(file)
    elif file.suffix in (".xls", ".xlsx"):
        df = pd.read_excel(file)
    else:
        raise ValueError("Invalid file format")
    return df.to_dict(orient='records')


parser = argparse.ArgumentParser(description='Process promotional data file')
parser.add_argument('inputfile', type=str, help='Path to the input file')
args = parser.parse_args()

initial = load_file(args.inputfile)

unprocessed_promos = []

exclude = [r"Earn \d+X Points*", r"Free with Purchase", r"\d+X Fuel Points"]

for item in initial:
    if any(re.search(exclude_item, item["digital_coupon_description"]) or re.search(exclude_item, item["volume_deals_description"]) for exclude_item in exclude):
        continue
    if not item["remarks"] and item["volume_deals_description"] and not item["volume_deals_price"]:
        unprocessed_promos.append(item)
        
    if item["digital_coupon_description"] and not item["digital_coupon_price"]:
        unprocessed_promos.append(item)
    
    if item["unit_price"] and item["unit_price"] < 0:
        unprocessed_promos.append(item)


print(len(unprocessed_promos))

if unprocessed_promos:
    output_file = Path(args.inputfile).stem + "_unprocessed.json"
    output_path = Path(args.inputfile).parent.parent / "issues" / output_file
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    with open(output_path, "w") as f:
        f.write(json.dumps(unprocessed_promos, indent=4))
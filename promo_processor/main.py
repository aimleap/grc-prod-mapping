from argparse import ArgumentParser
import json
from typing import List, Dict, Any
from promo_processor import PromoProcessor
from pathlib import Path
import pandas as pd
from datetime import datetime
from marianos import Marianos
from jewelosco import Jewelosco
from target import Target


class Processor:
    def __init__(self):
        self.args = self.parser()
        self.data = self.format_data(self.load_file())
        self.site = self.args.site

    def parser(self):
        parser = ArgumentParser()
        parser.add_argument("-f", "--file", help="File path")
        parser.add_argument("-o", "--output", help="Output directory", default="output")
        parser.add_argument("-s", "--site", help="Site Name", choices=['jewelosco', 'marianos', 'target'], required=True)
        parser.add_argument("-t", "--test", help="Test suite", action="store_true")
        return parser.parse_args()

    def load_file(self):
        file = Path(self.args.file)
        if not file.exists():
            raise FileNotFoundError(f"File {file} not found")
        if file.suffix == ".json":
            return pd.read_json(file)
        elif file.suffix == ".csv":
            return pd.read_csv(file)
        elif file.suffix in (".xls", ".xlsx"):
            return pd.read_excel(file)
        raise ValueError("Invalid file format")

    def load_site(self):
        if self.args.site == "jewelosco":
            return Jewelosco(PromoProcessor, self.data)
        elif self.args.site == "marianos":
            return Marianos(PromoProcessor, self.data)
        elif self.args.site == "target":
            return Target(PromoProcessor, self.data)
        raise ValueError("Invalid site")

    def format_data(self, data: pd.DataFrame) -> List[Dict[str, Any]]:
        data['upc'] = data['upc'].astype(str).str.zfill(13)
        data.fillna(value="", inplace=True)
        return data.to_dict(orient='records')

    def process(self):
        output_dir = Path(self.args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        processed_data = self.load_site()
        debug_dir = Path(__file__).parent / "debug"

        if not debug_dir.exists():
            debug_dir.mkdir(parents=True, exist_ok=True)

        with open(debug_dir / f"patterns_{datetime.now().date()}.json", "w") as f:
            patterns = processed_data.processor.site_patterns
            json.dump({self.site: patterns}, f, indent=4)

        if self.args.test:
            processed_data.processor.to_json(Path(output_dir) / f"{processed_data.__class__.__name__}_{datetime.now().date()}_test.json")
        else:
            processed_data.processor.to_json(Path(output_dir) / f"{processed_data.__class__.__name__}_{datetime.now().date()}.json")

def main():
    processor = Processor()
    processor.process()


if __name__ == "__main__":
    main()

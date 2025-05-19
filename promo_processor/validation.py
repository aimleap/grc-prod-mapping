from pydantic import BaseModel
from typing import Optional
from datetime import date
import argparse
import json
import sys
import re


class StoreProduct(BaseModel):
    zipcode: Optional[int]
    store_name: str
    store_location: str
    store_logo: str
    store_brand: str
    category: str
    sub_category: str
    product_title: str
    weight: str
    regular_price: Optional[float]
    sale_price: Optional[float]
    volume_deals_description: Optional[str]
    volume_deals_price: Optional[float]
    digital_coupon_description: Optional[str]
    digital_coupon_price: Optional[float]
    unit_price: Optional[float]
    image_url: str
    url: str
    upc: Optional[str]
    crawl_date: date
    remarks: Optional[str] = ""
    qc_remarks: Optional[str] = ""

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }

    @staticmethod
    def parse_float(value, field_name, qc_remarks):
        if value == '' or value is None:
            return 0
        try:
            return float(value)
        except ValueError:
            qc_remarks.append(f"{field_name} contains invalid value")
            return 0

    @staticmethod
    def validate_numeric_fields(data, qc_remarks):
        numeric_fields = ['regular_price', 'sale_price', 'volume_deals_price', 
                         'digital_coupon_price', 'unit_price']
        for field in numeric_fields:
            data[field] = StoreProduct.parse_float(data.get(field), field, qc_remarks)
        return data

    @staticmethod
    def validate_deals(data, qc_remarks, remarks):
        if data.get('unit_price') and data.get('sale_price') and (
            data.get('volume_deals_description') and (
                str(data.get('sale_price')) in data.get('volume_deals_description')
            ) or (data.get('sale_price') == data.get('unit_price'))
        ):
            qc_remarks.append('deals:passed')
            remarks.append("deals:promo already applied")

        if data.get('volume_deals_description') and not data.get('volume_deals_price') and not "deals:passed" in qc_remarks:
            qc_remarks.append('deals:fail')
            remarks.append('deals:unable to process promo/invalid promo')

    @staticmethod
    def validate_coupons(data, qc_remarks, remarks):
        if data.get('digital_coupon_description') and not data.get('digital_coupon_price'):
            qc_remarks.append('coupons:fail')
            remarks.append('coupons:unable to process promo/invalid promo')

    @staticmethod
    def validate_prices(data, qc_remarks):
        if data.get('sale_price') is not None and data.get('sale_price') >= data.get('regular_price', 0):
            qc_remarks.append('sale_price:fail')

        if data.get('unit_price') is not None:
            if any([data.get('digital_coupon_description'), data.get('volume_deals_description')]) and data.get('unit_price') <= 0:
                qc_remarks.append('unit_price:fail')
            if data.get('unit_price') < 0:
                qc_remarks.append('process:fail')
        
        if (data.get("volume_deals_description") or data.get("digital_coupon_description")) and not data.get("unit_price"):
            qc_remarks.append('unit_price:missing')

    @staticmethod
    def validate_metadata(data, qc_remarks):
        if not data.get('upc'):
            qc_remarks.append('upc:fail')

        if data.get('zipcode') and (len(str(data.get('zipcode'))) != 5):
            qc_remarks.append('zipcode:fail')

    @staticmethod
    def validate_promotions(data, qc_remarks):
        exclude_patterns = [r"Earn \d+X Points*", r"Free with Purchase", r"\d+X Fuel Points"]
        if data.get('digital_coupon_description') or data.get('volume_deals_description'):
            for pattern in exclude_patterns:
                if (data.get('digital_coupon_description') and re.search(pattern, data.get('digital_coupon_description'))) or \
                   (data.get('volume_deals_description') and re.search(pattern, data.get('volume_deals_description'))):
                    qc_remarks.append('excluded_promotion:fail')
                    break

    @staticmethod
    def validate_product(data):
        remarks = []
        qc_remarks = []

        data = StoreProduct.validate_numeric_fields(data, qc_remarks)
        StoreProduct.validate_deals(data, qc_remarks, remarks)
        StoreProduct.validate_coupons(data, qc_remarks, remarks)
        StoreProduct.validate_prices(data, qc_remarks)
        StoreProduct.validate_metadata(data, qc_remarks)
        StoreProduct.validate_promotions(data, qc_remarks)

        data['qc_remarks'] = '; '.join(qc_remarks) if qc_remarks else ""
        data['remarks'] = '; '.join(remarks) if remarks else ""
        return data


def format_zeros(data):
    keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
    for item in data:
        for key in keys:
            if item[key] == 0 or item[key] == 0.0:
                item[key] = ""
    return data


def process_product(item):
    item = StoreProduct.validate_product(item)
    product = StoreProduct(**item)
    product_dict = product.model_dump()
    product_dict['crawl_date'] = product_dict['crawl_date'].isoformat()
    return product_dict


def main():
    parser = argparse.ArgumentParser(description='Process store product data')
    parser.add_argument('input_file', help='Input JSON file path')
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            data = json.load(f)

        validated_products = [process_product(item) for item in data]

        with open(args.input_file.replace(".json", "_validated.json"), 'w') as f:
            json.dump(format_zeros(validated_products), f, indent=2)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
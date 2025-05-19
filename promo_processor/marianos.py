import re
from alive_progress import alive_it
from hashlib import sha256
import math,json
import pandas as pd
class Marianos:
    def __init__(self, processor, df):
        self.processor = processor
        self.deleteDescriptionCount = 0
        self.deleteDescriptionList = []
        self.processor.pre_process(self.getUniqueID)
        self.processor.pre_process(self.split_promos)
        self.processor.pre_process(self.sort_promos)
        self.processor.pre_process(self.split_promos_volume_description)
        # self.processor.pre_process(self.split_promos)
        self.processor.pre_process(self.remove_wrong_description)
        self.processor.process_item(df)
        self.processor.apply(self.get_lowest_valid_unit_price_item)
        self.processor.apply(self.skip_invalids)
        self.processor.apply(self.reorder_item)
        self.processor.apply(self.format_zeros)
        print("*****************************************************")
        print("self.deleteDescriptionCount :",self.deleteDescriptionCount)
        pd.DataFrame(self.deleteDescriptionList).to_csv("marianosDeletedDescription.csv")
        print("*****************************************************")

    def getUniqueID(self, data):
        new_data = []
        for item in data:
            # Make a hash key for the item excluding pricing-related fields
            item_copy = item.copy()
            for field in (
                "volume_deals_description",
                "volume_deals_price",
                "digital_coupon_description",
                "digital_coupon_price",
                "unit_price",
            ):
                item_copy.pop(field, None)

            item_hash = sha256(json.dumps(item_copy, sort_keys=True).encode()).hexdigest()
            item['item_hash'] = item_hash
            new_data.append(item)
        return new_data

    def sort_promos(self, data):
        patterns = [
        r"when\s+you\s+buy\s+1",                     # when you buy 1
            ]
        shiftFromDigitalToVolumn = ["[Bb]uy\s+(?P<buy>\d+),?\s+[Gg]et\s+(?P<free>\d+)\s+[Ff]ree"]
        # import pdb; pdb.set_trace()
        for item in data:
            # if any(re.search(pattern, item["volume_deals_description"],re.IGNORECASE) for pattern in patterns):
            #     if not item["digital_coupon_description"]:
            #         item["digital_coupon_description"] = item["volume_deals_description"]
            #     else:
            #         item["digital_coupon_description"] = item["digital_coupon_description"] + "||" + item["volume_deals_description"]
            #     item["volume_deals_description"] = ""

            if any(re.search(pattern, item["digital_coupon_description"],re.IGNORECASE) for pattern in shiftFromDigitalToVolumn):
                if not item["volume_deals_description"]:
                    item["volume_deals_description"] = item["digital_coupon_description"]
                else:
                    item["volume_deals_description"] = item["volume_deals_description"] + "||" + item["digital_coupon_description"]
                item["digital_coupon_description"] = ""
        return data

    def remove_invalid_promos(self, data):
        for item in data:
            description = item["description"]
            description = re.sub(r'\$\d+\.\d+/lb', '', description)
            description = re.sub(r'^about \$\d+\.\d+ each', '', description)
            description = re.sub(r'^\$\d+\.\d{2}', '', description)
            item["description"] = description.strip()
        return data

    def reorder_item(self, data):
        order = [
            "zipcode", "store_name", "store_location", "store_logo", "store_brand",
            "category", "sub_category", "product_title", "weight",
            "regular_price", "sale_price", "volume_deals_description",
            "volume_deals_price", "digital_coupon_description",
            "digital_coupon_price", "unit_price", "image_url", "url",
            "upc", "crawl_date", "remarks"
        ]
        return [{key: item.get(key, "") for key in order} for item in data if item]

    def split_promos(self, data):
        new_data = []
        for item in alive_it(data):
            if not item["digital_coupon_description"]:
                new_data.append(item.copy())
                continue
            promos = item["digital_coupon_description"].split("||")
            for promo in promos:
                item["digital_coupon_description"] = promo.strip()
                item["many"] = True
                new_data.append(item.copy())
        return new_data

    def split_promos_volume_description(self, data):
        new_data = []
        for item in alive_it(data):
            if not item["volume_deals_description"]:
                new_data.append(item.copy())
                continue
            promos = item["volume_deals_description"].split("||")
            for promo in promos:
                item["volume_deals_description"] = promo.strip()
                item["many"] = True
                new_data.append(item.copy())
        return new_data
    # def get_lowest_unit_price(self, data):
    #     if not data:
    #         return data
    #
    #     upc_dict = {}
    #
    #     for item in data:
    #         upc = item.get("upc")
    #         unit_price = float(item.get("unit_price", 0) or 0)
    #
    #         if upc not in upc_dict or (unit_price < float(upc_dict[upc].get("unit_price", 0) or 0) and unit_price > 0):
    #             upc_dict[upc] = item.copy()
    #
    #         if item.get("many"):
    #             del item["many"]
    #
    #     return list(upc_dict.values())

    # def get_lowest_unit_price(self, items):
    #     if not items:
    #         return {}
    #
    #     unique_items = {}
    #     for item in items:
    #         # build the hash key on everything except those deal/coupon/unit_price fields
    #         item_copy = item.copy()
    #         for k in (
    #             "volume_deals_description",
    #             "volume_deals_price",
    #             "digital_coupon_description",
    #             "digital_coupon_price",
    #             "unit_price",
    #         ):
    #             item_copy.pop(k, None)
    #
    #         item_hash = sha256(json.dumps(item_copy, sort_keys=True).encode()).hexdigest()
    #
    #         # parse this item's price
    #         try:
    #             curr_price = float(item.get("unit_price", 0) or 0)
    #         except (TypeError, ValueError):
    #             curr_price = math.inf
    #
    #         if item_hash not in unique_items:
    #             # first time we see this combination
    #             unique_items[item_hash] = item
    #
    #         else:
    #             # compare against the stored item's price
    #             old_item = unique_items[item_hash]
    #             try:
    #                 old_price = float(old_item.get("unit_price", 0) or 0)
    #             except (TypeError, ValueError):
    #                 old_price = math.inf
    #             if curr_price < old_price and curr_price > 0:
    #                 unique_items[item_hash] = item
    #     print("0000000000000000000000")
    #     print(len(unique_items))
    #     print("0000000000000000000000")
    #     unique_items_data = [unique_items[key] for key in unique_items]
    #     return unique_items_data
    def get_lowest_valid_unit_price_item(self,items):
        print(len(items))
        if not items:
            return []

        unique_items = {}

        for item in items:
            # print("Item hashes:", [item.get("item_hash") for item in items])

            # Make a hash key for the item excluding pricing-related fields
            item_copy = item.copy()
            """
            for field in (
                "volume_deals_description",
                "volume_deals_price",
                "digital_coupon_description",
                "digital_coupon_price",
                "unit_price",
            ):
                item_copy.pop(field, None)

            item_hash = sha256(json.dumps(item_copy, sort_keys=True).encode()).hexdigest()
            """
            item_hash = item.get("item_hash")
            # Try parsing unit_price
            try:
                unit_price = float(item.get("unit_price", 0) or 0)
                is_valid = unit_price > 0
            except (ValueError, TypeError):
                unit_price = 0
                is_valid = False

            # If this is the first time we've seen the item
            if item_hash not in unique_items:
                unique_items[item_hash] = item
                continue

            # Compare with stored item
            stored_item = unique_items[item_hash]
            try:
                stored_price = float(stored_item.get("unit_price", 0) or 0)
                stored_valid = stored_price > 0
            except (ValueError, TypeError):
                stored_price = 0
                stored_valid = False

            # Decide which item to keep
            if is_valid and (not stored_valid or unit_price < stored_price):
                unique_items[item_hash] = item
        print("(((((((((((((())))))))))))))")
        print(len(unique_items))
        print("(((((((((((((())))))))))))))")


        return list(unique_items.values())
    def skip_invalids(self, data):
        for item in data:
            sale_price = float(item.get("sale_price", 0) or 0)
            regular_price = float(item.get("regular_price", 0) or 0)
            unit_price = str(item.get("unit_price"))
            if unit_price !='':
                if float(item.get("unit_price")) and float(item["unit_price"]) < 0:
                    volume_deals_price = float(item.get("volume_deals_price", 0) or 0)
                    digital_coupon_price = float(item.get("digital_coupon_price", 0) or 0)

                    if volume_deals_price and (volume_deals_price > sale_price or volume_deals_price > regular_price or volume_deals_price == sale_price):
                        item.update({"volume_deals_price": ""})
        return data
    # def skip_invalids(self, data):
    #     print("skip_invalids", len(data))
    #
    #     for item in data:
    #         try:
    #             sale_price = float(item.get("sale_price") or 0)
    #             regular_price = float(item.get("regular_price") or 0)
    #             unit_price = item.get("unit_price")
    #
    #             # Clean up negative or invalid unit_price
    #             if unit_price and float(unit_price) < 0:
    #                 volume_deals_price = float(item.get("volume_deals_price") or 0)
    #
    #                 # Remove volume_deals_price if invalid
    #                 if volume_deals_price and (
    #                     volume_deals_price > sale_price or
    #                     volume_deals_price > regular_price or
    #                     volume_deals_price == sale_price
    #                 ):
    #                     item["volume_deals_price"] = ""
    #
    #             # Remove digital coupon if price is negative
    #             digital_coupon_price = float(item.get("digital_coupon_price") or 0)
    #             if digital_coupon_price < 0:
    #                 item["digital_coupon_price"] = ""
    #                 item["digital_coupon_description"] = ""
    #
    #         except (ValueError, TypeError) as e:
    #             print(f"Error processing item {item}: {e}")
    #             continue
    #
    #     print("completed skip_invalids", len(data))
    #     return data


    def format_zeros(self, data):
        keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
        for item in data:
            for key in keys:
                if item[key] == 0:
                    item[key] = ""
        return data

    # def should_skip_item(self,item_title):
    #     skip_keywords = ["chips", "tortilla","grab & go","turkey bundle","when you buy 1 ",'cutwater','gold peak','coors banq']
    #     return any(word in item_title.lower() for word in skip_keywords)
    #
    # def remove_wrong_description(self, data):
    #     keys = ['volume_deals_description']
    #     for item in data:
    #         for key in keys:
    #             value = item.get(key)
    #             if self.should_skip_item(value):
    #                 item['volume_deals_description'] = ""
    #                 self.deleteDescriptionCount+=1
    #                 self.deleteDescriptionList.append({"deleteDescriptionCount":self.deleteDescriptionCount,"deleteDescriptionText":value,'upc':item['upc']})
    #              # Check if the original string ends with exactly "when you buy 1" (case-sensitive)
    #             ends_with_when_you_buy_1 = value.endswith("when you buy 1")
    #             if ends_with_when_you_buy_1:
    #                 item['volume_deals_description'] = ""
    #                 self.deleteDescriptionCount+=1
    #                 self.deleteDescriptionList.append({"deleteDescriptionCount":self.deleteDescriptionCount,"deleteDescriptionText":value,'upc':item['upc']})
    #     return data

    import re

    def should_skip_item(self, item_title):
        skip_keywords = [
            "chips", "tortilla", "grab & go", "turkey bundle",
             "cutwater", "gold peak", "coors banq"
        ]
        item_title_lower = item_title.lower()
        return any(keyword in item_title_lower for keyword in skip_keywords)

    def matches_save_spend_pattern(self, text):
        # Regex for "Save $10 when you spend $40", allowing any dollar amounts
        pattern = r"save\s*\$\d+\s*when you spend\s*\$\d+"
        return bool(re.search(pattern, text, re.IGNORECASE))

    def remove_wrong_description(self, data):
        keys = ['volume_deals_description']
        for item in data:
            for key in keys:
                value = item.get(key)
                if not value:
                    continue

                should_delete = (
                    self.should_skip_item(value) or
                    value.strip().lower().endswith("when you buy 1") or
                    self.matches_save_spend_pattern(value) or value.strip().lower().endswith("buy 1, save $1")
                )

                if should_delete:
                    item['volume_deals_description'] = ""
                    self.deleteDescriptionCount += 1
                    self.deleteDescriptionList.append({
                        "deleteDescriptionCount": self.deleteDescriptionCount,
                        "deleteDescriptionText": value,
                        "upc": item.get('upc')
                    })
                    self.deleteDescriptionList.append({"deleteDescriptionCount":self.deleteDescriptionCount,"deleteDescriptionText":value,'upc':item['upc']})
        return data

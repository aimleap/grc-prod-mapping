import re
from alive_progress import alive_it
from hashlib import sha256
import math,json
import pandas as pd

# Your dictionary
NUMBER_MAPPING = {
    "ONE": 1, "TWO": 2, "THREE": 3, "FOUR": 4, "FIVE": 5,
    "SIX": 6, "SEVEN": 7, "EIGHT": 8, "NINE": 9, "TEN": 10
}

# Function to replace number words
def replace_number_words(text):
    if not isinstance(text, str):
        return text  # If it's not a string, return as-is
    pattern = r'\b(' + '|'.join(NUMBER_MAPPING.keys()) + r')\b'
    return re.sub(pattern, lambda m: str(NUMBER_MAPPING[m.group(0).upper()]), text, flags=re.IGNORECASE)

class Jewelosco:
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
        self.processor.pre_process(self.remove_wrong_description_from_digital_coupon)
        self.processor.pre_process(self.numberMapping)
        self.processor.process_item(df)
        self.processor.apply(self.get_lowest_valid_unit_price_item)
        self.processor.apply(self.skip_invalids)
        self.processor.apply(self.remove_price_when_weight_is_approx)
        self.processor.apply(self.reorder_item)
        self.processor.apply(self.format_zeros)
        print("*****************************************************")
        print("self.deleteDescriptionCount :",self.deleteDescriptionCount)
        pd.DataFrame(self.deleteDescriptionList).to_csv("jeweloscoDeletedDescription.csv")
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

    def numberMapping(self, data):
        keys = ['volume_deals_description',"digital_coupon_description"]
        new_data = []
        for item in data:
            for key in keys:
                value = item.get(key)
                item[key] = replace_number_words(value)
            new_data.append(item)
        return new_data

    def sort_promos(self, data):
        patterns = [
        r'(\d+)\s*for\s*\$(\d+\.?\d*)',                     # 2 for $5, 3 for $10
        r'Buy\s*(\d+)\s*Get\s*(\d+)\s*Free',                # Buy 1 Get 1 Free, Buy 2 Get 1 Free
        r'Buy\s*(\d+),?\s*Get\s*(\d+)\s*at\s*(\d+)%\s*off',   # Buy 1 Get 1 50% off, Buy 2 Get 1 25% off
        # r'Buy\s*(\d+),?\s*get\s*(\d+)\s*(?:at\s*)?(\d+)%\s*off', #Buy 1, get 1 25% off select beauty products'
        r'Buy\s*(\d+),?\s*get\s*(\d+)\s*free',#Buy 3, get 1 free on select beauty mini's
        # ✅ NEW pattern for "$X Save Up To: $Y"
        r'\$(\d+\.\d{1,2})\s*Save Up To:\s*\$(\d+\.\d{1,2})',
        r"(?i)buy\s+1\s+get\s+1\s+(?P<percent>\d+)%\s+off",
        r"when\s+you\s+buy\s+",                     # when you buy
        # r"off\s+Limit\s+(?P<limit>\d+)",
        r"Buy\s+(?P<buy_qty>\d+)\s+Get\s+(?P<get_qty>\d+)\s+\$(?P<discount>\d+(?:\.\d{1,2})?)\s+Off",
        "(?i)\$(\d+(?:\.\d{1,2})?)\s*off\s*when\s*(?:you\s*)?buy\s*(?:[A-Z]+\()?(\d+)\)?" ,

        # r"\$(?P<discount>\d+\.\d{1,2})\s+off\s+Limit\s+(?P<limit1>\d+)\s+(?P<size>\d+-\d+-oz\.)\s+Limit\s+(?P<limit2>\d+)" #"$0.50 off Limit 1 8-20-oz. Limit 1."

        # r"\$\d+\.\d{2} off When Buy \d+ Limit \d+ When you buy"

            ]
        patternsToCheckVolumeDeal = [
        r"\$(?P<discount>\d+\.\d{1,2})\s+off\s+When\s+Buy\s+(?P<buy_qty>\d+)\s+Limit\s+(?P<limit>\d+)\s+When\s+you\s+buy"
        ]

        skipKeyword = ['when you buy one']
        # skipKeyword = ['when you buy one','limit 1']
        for item in data:

            # if not any(re.search(pattern, item["volume_deals_description"],re.IGNORECASE) for pattern in patterns):
            #     if not item["digital_coupon_description"]:
            #         item["digital_coupon_description"] = item["volume_deals_description"]
            #     else:
            #         if item["volume_deals_description"]:
            #             item["digital_coupon_description"] = item["digital_coupon_description"] + "||" + item["volume_deals_description"]
            #     item["volume_deals_description"] = ""
            if any(re.search(pattern, item["digital_coupon_description"],re.IGNORECASE) for pattern in patterns):
                if not any(word in item["digital_coupon_description"].lower() for word in skipKeyword):
                    if not item["volume_deals_description"]:
                        item["volume_deals_description"] = item["digital_coupon_description"]
                    else:
                        item["volume_deals_description"] = item["volume_deals_description"] + "||" + item["digital_coupon_description"]
                    item["digital_coupon_description"] = ""
            elif "limit 1" not in item["digital_coupon_description"].lower():
                if "when you buy" in item["digital_coupon_description"].lower():
                    if not item["volume_deals_description"]:
                        item["volume_deals_description"] = item["digital_coupon_description"]
                    else:
                        if "Wine 10%" not in item["volume_deals_description"]:
                            item["volume_deals_description"] = item["volume_deals_description"] + "||" + item["digital_coupon_description"]
                        else:
                            item["volume_deals_description"] = item["digital_coupon_description"]
                    item["digital_coupon_description"] = ""

            # if any(re.search(pattern, item["volume_deals_description"],re.IGNORECASE) for pattern in patternsToCheckVolumeDeal):
            #     if not item["digital_coupon_description"]:
            #         item["digital_coupon_description"] = item["volume_deals_description"]
            #     else:
            #         if item["volume_deals_description"]:
            #             item["digital_coupon_description"] = item["digital_coupon_description"] + "||" + item["volume_deals_description"]
            #     item["volume_deals_description"] = ""
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
        for item in data:
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
    #         if upc not in upc_dict or unit_price < float(upc_dict[upc].get("unit_price", 0) or 0):
    #             upc_dict[upc] = item.copy()
    #
    #         if item.get("many"):
    #             del item["many"]
    #
    #     return list(upc_dict.values())
    # def get_lowest_unit_price(self, items):
    #     print(items)
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
        if not items:
            return []

        unique_items = {}

        for item in items:
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
        print(len(unique_items))

        return list(unique_items.values())


    def skip_invalids(self, data):
        for item in data:
            sale_price = float(item.get("sale_price", 0) or 0)
            regular_price = float(item.get("regular_price", 0) or 0)
            if item.get("unit_price") and item["unit_price"] < 0:
                volume_deals_price = float(item.get("volume_deals_price", 0) or 0)
                digital_coupon_price = float(item.get("digital_coupon_price", 0) or 0)
                if volume_deals_price and (volume_deals_price > sale_price or volume_deals_price > regular_price or volume_deals_price == sale_price):
                    item.update({"volume_deals_price": ""})

            # if volume_deals_price == sale_price:
                # item.update({"volume_deals_price": ""})
        return data

    def format_zeros(self, data):
        keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
        # for item in data:
        #     for key in keys:
        #         if item[key] == 0:
        #             item[key] = ""
        for item in data:
            for key in keys:
                value = item.get(key)
                if value == 0:
                # if isinstance(value, (int, float)) and value == 0:
                    item[key] = ""
                elif isinstance(value, (int, float)):
                    item[key] = "{:.2f}".format(value)

        return data


    def remove_price_when_weight_is_approx(self, data):
        keys = ['weight']
        for item in data:
            for key in keys:
                value = item.get(key)
                if "approx" in str(value).lower():
                    if "lb" in item['volume_deals_description'].lower():
                        item['volume_deals_price'] = 0
                        item['digital_coupon_price'] = 0
                        item['unit_price'] = 0
        return data

    def should_skip_item(self,item_title):
        skip_keywords = ["save:","rebate available",'signature select graham crackers or marshmallows']
        # skip_keywords = ["healthy aisles","save:","signature sale","lb save up to","rebate available"]
        return any(word in item_title.lower() for word in skip_keywords)

    # def remove_wrong_description(self, data):
    #     keys = ['volume_deals_description']
    #     for item in data:
    #         for key in keys:
    #             value = item.get(key)
    #             if self.should_skip_item(value):
    #                 item['volume_deals_description'] = ""
    #             elif "save up to" in value.lower():
    #                 if "for" not in value.lower():
    #                     item['volume_deals_description'] = ""
    #     return data
    #
    def remove_wrong_description(self, data):
        # ['Save Up To:'
        keys = ['volume_deals_description']
        for item in data:
            for key in keys:
                value = item.get(key)
                if self.should_skip_item(value):
                    item['volume_deals_description'] = ""
                    self.deleteDescriptionCount+=1
                    self.deleteDescriptionList.append({"deleteDescriptionCount":self.deleteDescriptionCount,"deleteDescriptionText":value,'upc':item['upc']})
                elif "for" not in str(value).lower():
                    if "Save Up To".lower() in str(value).lower():
                        item['volume_deals_description'] = ""
                        self.deleteDescriptionCount+=1
                        self.deleteDescriptionList.append({"deleteDescriptionCount":self.deleteDescriptionCount,"deleteDescriptionText":value,'upc':item['upc']})
        return data

    def remove_wrong_description_from_digital_coupon(self, data):
        # ['Save Up To:'
        # skip_keywords = ['when you spend','earn 4x','schedule & save','free signature','earn','free']
        skip_keywords = ['when you spend','earn 4x','schedule & save','free signature','earn','free marshmallows', 'free limit', 'free cheetos macaroni',"when you buy one"]
        keys = ['digital_coupon_description']
        print(len(data))
        for item in data:
            for key in keys:
                value = item.get(key)
                if any(word in value.lower() for word in skip_keywords):
                    item['digital_coupon_description'] = ""
                    self.deleteDescriptionCount+=1
                    self.deleteDescriptionList.append({"deleteDescriptionCount":self.deleteDescriptionCount,"deleteDescriptionText":value,"upc":item['upc']})
        print(len(data))

        return data

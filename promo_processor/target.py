import re
import pandas as pd
import json
from hashlib import sha256
import math

class Target:
    def __init__(self, processor, df):
        self.processor = processor
        self.deleteDescriptionCount = 0
        self.deleteDescriptionList = []
        self.processor.pre_process(self.split_promos)
        self.processor.pre_process(self.sort_promos)
        self.processor.pre_process(self.split_promos)
        self.processor.pre_process(self.remove_wrong_description)
        self.processor.process_item(df)
        self.processor.apply(self.reorder_item)
        self.processor.apply(self.skip_invalids)
        self.processor.apply(self.get_lowest_unit_price)
        self.processor.apply(self.format_zeros)
        self.processor.apply(self.format_date)
        print("*****************************************************")
        print("self.deleteDescriptionCount :",self.deleteDescriptionCount)
        pd.DataFrame(self.deleteDescriptionList).to_csv("targetDeletedDescription.csv")
        print("*****************************************************")

    def sort_promos(self, data):
        patterns = [
            r'(\d+)\s*for\s*\$(\d+\.?\d*)',                     # 2 for $5, 3 for $10
            r'(\d+)\s*@\s*\$(\d+\.?\d*)',                       # 2 @ $5, 3 @ $10
            r'(\d+)\s*\/\s*\$(\d+\.?\d*)',                      # 2/$5, 3/$10
            r'Buy\s*(\d+)\s*Get\s*(\d+)\s*Free',                # Buy 1 Get 1 Free, Buy 2 Get 1 Free
            r'Buy\s*(\d+)\s*Get\s*(\d+)\s*at\s*(\d+)%\s*off',   # Buy 1 Get 1 50% off, Buy 2 Get 1 25% off
            r'Buy\s*(\d+)\s*save\s*\$(\d+\.?\d*)',              # Buy 2 Save $5, Buy 3 Save $10
            r'Buy\s*(\d+)\s*save\s*(\d+)%\s*off',
            r'Mix\s*&\s*Match\s*(\d+)\s*for\s*\$(\d+\.?\d*)',   # Mix & Match 2 for $5, Mix & Match 3 for $10
            r'Save\s*\$(\d+\.?\d*)\s*when\s*you\s*buy\s',       # Save $5 when you buy, Save $10 when you buy
            r'Buy\s*(\d+),?\s*get\s*(\d+)\s*(?:at\s*)?(\d+)%\s*off', #Buy 1, get 1 25% off select beauty products'
            r'Buy\s*(\d+),?\s*get\s*(\d+)\s*free',#Buy 3, get 1 free on select beauty mini's
            # r"Save\s+(\d+)%\s+with\s+$(\d+)",  #Save 20% with
            r"Save\s+\$(\d+)\s+with\s+\$(\d+)", #Save $20 with $30
            # r"Save\s+(\d+)%\s+with\s+$(\d+)",  #Save 20% with
            # r'$(\d+)\s+price\s+each\s+with\s+(\d+)'
            r"\$(\d+(?:\.\d{2})?)\s*(?:price\s*)?each\s*with\s*(\d+)\s*select\s+(.+?)\s*on\s+select\s+items", #"$9.99 price each with 2 select coffee on select items"ss
            # r"^Save\s+(?P<discount>\d+)%\s+on\s+(?P<product>[\w\s-]+)",
            r"\$\d{1,3}(?:\.\d{2})?\s+price\s+each\s+with\s+\d+\s+select\s+coffee\s+items", #"$15 price each with 10 select coffee items"

            "(?i)buy\s*(\d+)[\.,]?\s*get\s*(\d+)\s*(\d+)%\soff\sselect\sbeloved\spersonal\scare\sitems", #"Buy 1. get 1 50% off select Beloved personal care items"
            "(?i)Save\s*(?P<discount>\d+)%\s*on\s*(?P<quantity>\d+)\s*select\s*(?P<item_description>.+)", #"Save 25% on 3 select beverages"
            "(?i)buy\s*(\d+)[\.,]?\s*get\s*(\d+)\s*(\d+)%\soff\s", #"Buy 1. get 1 50% off"

            ]
        # pattern2 = [
            # r"^Save\s+(?P<discount>\d+)%\s+on\s+select+\s",
        # ]

        print("sort_promos started",len(data))

        for item in data:
            # if not any(re.search(pattern, item["volume_deals_description"]) for pattern in patterns):
            #     if not item["digital_coupon_description"]:
            #         item["digital_coupon_description"] = item["volume_deals_description"]
            #     else:
            #         if  item["volume_deals_description"]:
            #             item["digital_coupon_description"] = item["digital_coupon_description"] + "||" + item["volume_deals_description"]
            #     item["volume_deals_description"] = ""

            if any(re.search(pattern, item["digital_coupon_description"]) for pattern in patterns):
                if not item["volume_deals_description"]:
                    item["volume_deals_description"] = item["digital_coupon_description"]
                else:
                    item["volume_deals_description"] = item["volume_deals_description"] + "||" + item["digital_coupon_description"]
                item["digital_coupon_description"] = ""

            # if any(re.search(pattern, item["volume_deals_description"]) for pattern in pattern2):
            #     if not item["digital_coupon_description"]:
            #         item["digital_coupon_description"] = item["volume_deals_description"]
            #     else:
            #         item["digital_coupon_description"] = item["digital_coupon_description"] + "||" + item["volume_deals_description"]
            #     item["volume_deals_description"] = ""
        # print("sort_promos completed",len(data))

        return data

    def should_skip_description(self,item_title):
        skip_keywords = ["select first aid","in cart on la",'target giftcard','free phone charm','select personal care purchase']
        return any(word in item_title.lower() for word in skip_keywords)

    def remove_invalid_promos(self, data):
        for item in data:
            description = item["description"]
            description = re.sub(r'\$\d+\.\d+/lb', '', description)
            description = re.sub(r'^about \$\d+\.\d+ each', '', description)
            description = re.sub(r'^\$\d+\.\d{2}', '', description)
            item["description"] = description.strip()
        return data

    def reorder_item(self, data):
        print("reorder_item :",len(data))
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
        print("promo splited",len(data))
        new_data = []
        for item in data:
            if not item["digital_coupon_description"]:
                new_data.append(item.copy())
                continue
            promos = item["digital_coupon_description"].split("||")
            if len(promos)>1:
                print(item['upc'])
            for promo in promos:
                item["digital_coupon_description"] = promo.strip()
                item["many"] = True
                new_data.append(item.copy())
        print("after promo splited",len(new_data))
        return new_data

    # def get_lowest_unit_price(self, data):
    #
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
    #     return list(upc_dict.values())

    def skip_invalids(self, data):
        print("skip_invalids ",len(data))
        for item in data:
            sale_price = float(item.get("sale_price", 0) or 0)
            regular_price = float(item.get("regular_price", 0) or 0)

            if item.get("unit_price") and item["unit_price"] < 0:
                volume_deals_price = float(item.get("volume_deals_price", 0) or 0)
                digital_coupon_price = float(item.get("digital_coupon_price", 0) or 0)

                if volume_deals_price and (volume_deals_price > sale_price or volume_deals_price > regular_price or volume_deals_price == sale_price):
                    item.update({"volume_deals_price": ""})

        print("completed skip_invalids ",len(data))

        return data

    # def format_zeros(self, data):
    #     keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
    #     for item in data:
    #         for key in keys:
    #             if item[key] == 0:
    #                 item[key] = ""
    #
    #     return data

    def format_date(self, data):
        df = pd.DataFrame(data)
        df['crawl_date'] = df['crawl_date'].astype(str)
        return df.to_dict(orient='records')

    # def get_lowest_unit_price(self, data):
    #     if not data:
    #         return data
    #     upc_dict = {}
    #     print("get_lowest_unit_price",len(data))
    #     for item in data:
    #         upc = item.get("upc")
    #         unit_price = float(item.get("unit_price", 0) or 0)
    #
    #         if upc not in upc_dict or unit_price < float(upc_dict[upc].get("unit_price", 0) or 0) and item.get("many"):
    #             upc_dict[upc] = item.copy()
    #
    #         if item.get("many"):
    #             del item["many"]
    #     print("get_lowest_unit_price ")
    #     print(len(upc_dict))
    #
    #     return list(upc_dict.values())
    # def get_lowest_unit_price(self, items):
    #     if not items:
    #         return {}
    #     unique_items = {}
    #     for item in items:
    #         item_copy = item.copy()
    #         del item_copy["volume_deals_description"]
    #         del item_copy["volume_deals_price"]
    #         del item_copy["digital_coupon_description"]
    #         del item_copy["digital_coupon_price"]
    #         del item_copy["unit_price"]
    #
    #         item_hash = sha256(json.dumps(item_copy, sort_keys=True).encode()).hexdigest()
    #         if item_hash not in unique_items or item['unit_price'] < unique_items[item_hash]['unit_price']:
    #             unique_items[item_hash] = item
    #     return unique_items


    def get_lowest_unit_price(self, items):
        if not items:
            return {}

        unique_items = {}
        for item in items:
            # build the hash key on everything except those deal/coupon/unit_price fields
            item_copy = item.copy()
            for k in (
                "volume_deals_description",
                "volume_deals_price",
                "digital_coupon_description",
                "digital_coupon_price",
                "unit_price",
            ):
                item_copy.pop(k, None)

            item_hash = sha256(json.dumps(item_copy, sort_keys=True).encode()).hexdigest()

            # parse this item's price
            try:
                curr_price = float(item.get("unit_price", 0) or 0)
            except (TypeError, ValueError):
                curr_price = math.inf

            if item_hash not in unique_items:
                # first time we see this combination
                unique_items[item_hash] = item

            else:
                # compare against the stored item's price
                old_item = unique_items[item_hash]
                try:
                    old_price = float(old_item.get("unit_price", 0) or 0)
                except (TypeError, ValueError):
                    old_price = math.inf
                if curr_price < old_price and curr_price > 0:
                    unique_items[item_hash] = item
        print("0000000000000000000000")
        print(len(unique_items))
        print("0000000000000000000000")
        unique_items_data = [unique_items[key] for key in unique_items]
        return unique_items_data

    # def skip_invalids(self, data):
    #     for item in data:
    #         sale_price = float(item.get("sale_price", 0) or 0)
    #         regular_price = float(item.get("regular_price", 0) or 0)
    #
    #         if item.get("unit_price") and item["unit_price"] < 0:
    #             volume_deals_price = float(item.get("volume_deals_price", 0) or 0)
    #             digital_coupon_price = float(item.get("digital_coupon_price", 0) or 0)
    #
    #             if volume_deals_price and (volume_deals_price > sale_price or volume_deals_price > regular_price or volume_deals_price == sale_price):
    #                 item.update({"volume_deals_price": ""})
    #     return data

    def format_zeros(self, data):
        keys = ["regular_price", "sale_price", "volume_deals_price", "digital_coupon_price", "unit_price"]
        for item in data:
            for key in keys:
                if item[key] == 0:
                    item[key] = ""
        return data

    def remove_wrong_description(self, data):
        # ['Save Up To:'
        keys = ['volume_deals_description','digital_coupon_description']
        for item in data:
            for key in keys:
                value = item.get(key)
                if self.should_skip_description(value):
                    item[key] = ""
                    self.deleteDescriptionCount+=1
                    self.deleteDescriptionList.append({"deleteDescriptionCount":self.deleteDescriptionCount,"deleteDescriptionText":value,'upc':item['upc']})
        return data

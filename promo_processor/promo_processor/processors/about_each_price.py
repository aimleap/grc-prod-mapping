from promo_processor.processor import PromoProcessor

# def should_skip_item(item_title):
#     skip_keywords = ["chips", "tortilla","grab & go"]
#     return any(word in item_title.lower() for word in skip_keywords)

class AboutEachPriceProcessor(PromoProcessor, version=1):
    patterns = [r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s",
    r"\$(?P<unit_price>\d+(?:\.\d{1,2})?)\s+each\s+\d+-\d+-oz\.\s+when\s+you\s+buy\s+(?P<quantity>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s+limit\s+(?P<min_quantity>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+limit\s+(?P<quantity>\d+)\s+.*?limit\s+(?P<min_quantity>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+Each",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s+or\s+more",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each\.\s+when\s+you\s+buy\s+(?P<quantity>\d+)\.\s+limit\s+(?P<limit>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.*?limit\s+(?P<limit>\d+)",
                "\$(?P<unit_price>\d+(?:\.\d{1,2})?)\s*each\s*when\s*you\s*buy\s*(?P<quantity>\d+)(?:.*?)limit\s*(?P<limit>\d+)"


]


    # Example: "$5.99 Each" or "$2.50 Each"

    def calculate_deal(self, item, match):
        item_data = item.copy()
        unit_price = float(match.group('unit_price'))
        # unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        try:
            quantity = int(match.group('quantity'))
        except:
            try:
                quantity = int(match.group('limit'))
            except:
                quantity = item_data.get("quantity", 1)

        try:
            discount = float(match.group('unit_price'))
        except:
            discount = item_data.get("unit_price", 0)
        # volume_deals_price = (discount * quantity) #- discount
        volume_deals_price = (unit_price * quantity) #- discount
        unit_price_calculated = float(volume_deals_price) / quantity
        # item_title = item_data.get("volume_deals_description")
        # if should_skip_item(item_title):
        #     item_data['volume_deals_price'] = 0
        #     item_data['unit_price'] = 0
        #     print("Skipping item – promo/free item:", item_title)
        # else:
        item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price_calculated, 2)
        item_data['digital_coupon_price'] = 0

        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()

        unit_price = float(match.group('unit_price'))
        # quantity = item_data.get("quantity", 1)
        try:
            quantity = int(match.group('quantity'))
        except:
            try:
                quantity = int(match.group('limit'))
            except:
                quantity = item_data.get("quantity", 1)
        volume_deals_price = unit_price * quantity
        unit_price_calculated = volume_deals_price / quantity
        digital_coupon_price = unit_price * quantity
        item_data['digital_coupon_price'] = round(digital_coupon_price, 2)
        # item_data['digital_coupon_price'] = round(unit_price_calculated, 2)

        item_data["unit_price"] = round(unit_price_calculated, 2)

        return item_data

class SaveEachWhenBuyMoreProcessor(PromoProcessor, version=2):
    patterns = [r"Save\s+\$(?P<discount>\d+(?:\.\d+)?)\s+each\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)\s+or\s+more"]
    # Save $1 each when you buy 5 or more
    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount = float(match.group('discount'))
        min_quantity = int(match.group('min_quantity'))
        # quantity = item_data.get("quantity", 1)
        try:
            quantity = int(match.group('quantity'))
        except:
            quantity = int(item_data.get("quantity", 1))
        original_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)


        volume_deals_price = discount * min_quantity
        original_price = float(original_price)
        unit_price = ((original_price * min_quantity) - volume_deals_price) / min_quantity

        volume_deals_priceNew = (original_price * min_quantity) - volume_deals_price

        item_data['volume_deals_price'] = round(volume_deals_priceNew, 2)
        if unit_price < 0:
            item_data['unit_price'] = ""
        else:
            item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount = float(match.group('discount'))
        min_quantity = int(match.group('min_quantity'))
        # quantity = item_data.get("quantity", 1)
        try:
            quantity = int(match.group('quantity'))
        except:
            quantity = item_data.get("quantity", 1)
        original_price = item_data.get("unit_price", 0)

        if quantity >= min_quantity:
            discounted_price = (original_price *quantity ) - discount
            # discounted_price = original_price - discount
            item_data['digital_coupon_price'] = round(discounted_price, 2)
            item_data["unit_price"] = round(discounted_price, 2)

        return item_data



# r"Buy\s+(?P<buy_quantity>\d+)\s+Grab\s+&\s+Go\s+Sandwich\s+&\s+Get\s+(?P<get_quantity>\d+)\s+(?P<get_item>.+?)\s+for\s+\$(?P<unit_price>\d+(?:\.\d+)?)\s+each"

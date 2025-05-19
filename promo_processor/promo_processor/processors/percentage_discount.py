from promo_processor.processor import PromoProcessor

class PercentageOffProcessor(PromoProcessor, version=1):
    patterns = [
        # r"^(?P<discount>\d+)%\s+off",
        r"^(?P<discount>\d+)%\s+off(?!\s*[\w\s]+)",  # Does not match if followed by extra words (like "When Buy")
        # r"^(?P<discount>\d+)%\s+of",
        r"^(?P<discount>\d+)%\s+of(?!\s*[\w\s]+)",   # Does not match if followed by extra words
        r"^(?P<discount>\d+)%\s+select",
        r"^Deal:\s+(?P<discount>\d+)%\s+off",
        r"^Save\s+(?P<discount>\d+)%$",
        r"^Save\s+(?P<discount>\d+)%\s+on",
        r"^Save\s+(?P<discount>\d+)%",
        r"(?i)(?P<discount>\d+)%\s*off.*?buy\s+(?P<product>\d+).*?(?P<name>[\w\s.-]*)?"


    ]

    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        # import pdb; pdb.set_trace()
        if "product" in match.groupdict().keys():
            quantity = float(match.group('product'))
            per_product = price * quantity
            discount_amount = per_product*discount_decimal
            digital_coupon_price = per_product - discount_amount
            unit_price = digital_coupon_price/quantity
            item_data["unit_price"] = round(unit_price, 2)
            item_data["volume_deals_price"] = round(digital_coupon_price, 2)
        else:
            discounted_price = price * (1 - discount_decimal)
            unit_price = discounted_price
            item_data["volume_deals_price"] = round(discounted_price, 2)
            item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0
        if "product" in match.groupdict().keys():
            quantity = float(match.group('product'))
            per_product = base_price * quantity
            discount_amount = per_product*discount_decimal
            digital_coupon_price = per_product - discount_amount
            unit_price = digital_coupon_price/quantity
            item_data["unit_price"] = round(unit_price, 2)
            item_data["digital_coupon_price"] = round(digital_coupon_price, 2)
        else:
            discounted_price = base_price * (1 - discount_decimal)
            item_data["unit_price"] = round(discounted_price, 2)
            item_data["digital_coupon_price"] = round(discounted_price, 2)
        return item_data

class PercentageOffProductProcessor(PromoProcessor, version=2):
    patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+on\s+(?P<product>[\w\s-]+)",
        r"^Save\s+(?P<discount>\d+)%\s+on\s+(?P<product>[\w\s-]+)\s+select",
        r"^Save\s+(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
        r"^(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
        r"(?i)(?P<discount>\d+)%\s*off\s*when\s*you\s*buy\s*(?P<product>\d+)"

    ]

    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0
        try:
            product_qty = float(match.group('product'))
        except:
            product_qty = item_data.get("product", 1)
        """
        discounted_price = price * (1 - discount_decimal)
        unit_price = discounted_price
        volume_deals_price = (price * product_qty) - discounted_price
        """
        per_product = price * product_qty
        discount_amount = per_product * discount_decimal
        volume_deals_price = per_product - discount_amount
        unit_price = volume_deals_price/product_qty
        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        # item_data["volume_deals_price"] = round(volume_deals_price, 2)
        # item_data["volume_deals_price"] = round(discounted_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        """ old logic
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0

        discounted_price = base_price * (1 - discount_decimal)
        item_data["unit_price"] = round(discounted_price, 2)
        item_data["digital_coupon_price"] = round(discounted_price, 2)
        """
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0

        discount_percent = float(match.group('discount'))
        try:
            product = float(match.group('product'))
        except:
            product = item_data.get("product", 1)
        discount_amount = round(base_price * (discount_percent / 100), 2)
        final_price = round(base_price - discount_amount, 2)

        digital_coupon_price = (base_price * product) - discount_amount

        item_data["unit_price"] = round(final_price, 2)
        item_data["digital_coupon_price"] = round(digital_coupon_price, 2)
        # item_data["digital_coupon_price"] = round(discount_amount, 2)
        return item_data

class PercentageOffQuantityProcessor(PromoProcessor, version=3):
    patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+with\s+(?P<quantity>\d+)",
        r"^Save\s+(?P<discount>\d+)%\s+each\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s+or\s+more",

    ]

    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100

        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0

        quantity = int(match.group('quantity'))
        if "or more" in match.string:
            item_data["min_quantity"] = quantity
            # discounted_price = price * (1 - discount_decimal)
            # unit_price = discounted_price
        # else:
        #     total_price = price * quantity
        #     discounted_price = total_price * (1 - discount_decimal)
        #     unit_price = discounted_price / quantity
        per_product = price * quantity
        discount_amount = per_product*discount_decimal
        volume_deals_price = per_product - discount_amount
        unit_price = volume_deals_price/quantity

        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0

        discounted_price = base_price * (1 - discount_decimal)

        item_data["unit_price"] = round(discounted_price, 2)
        item_data["digital_coupon_price"] = round(discounted_price, 2)
        return item_data


class PercentageOffSelectProcessor(PromoProcessor, version=4):
    patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+select",
    ]

    def calculate_deal(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        price = item_data.get("sale_price") or item_data.get('regular_price', 0)
        price = float(price) if price else 0

        discounted_price = price * (1 - discount_decimal)

        item_data["volume_deals_price"] = round(discounted_price, 2)
        item_data["unit_price"] = round(discounted_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        discount_percentage = float(match.group('discount'))
        discount_decimal = discount_percentage / 100
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        base_price = float(base_price) if base_price else 0

        discounted_price = base_price * (1 - discount_decimal)

        item_data["unit_price"] = round(discounted_price, 2)
        item_data["digital_coupon_price"] = round(discounted_price, 2)
        return item_data

from promo_processor.processor import PromoProcessor

class PriceEachWithQuantityProcessor(PromoProcessor, version=1):
    """Processor for handling '$X price each with Y' type promotions."""

    # patterns = [r'\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+each\s+(?:when\s+you\s+buy|with|for)\s+(?P<quantity>\d+)',
    # r'\$(?P<price>\d+(?:\.\d{2})?)\s*ea\.?\s*(?:when\s+you\s+buy|when\s+buy)\s+(?P<quantity>\d+)\s+or\s+more'
    # ]
    patterns = [
    r'\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+each\s+(?:when\s+you\s+buy|with|for)\s+(?P<quantity>\d+)',
    ]




    def calculate_deal(self, item, match):
        """Process '$X price each with Y' type promotions for deals."""
        item_data = item.copy()
        price_each = float(match.group('price'))
        quantity = int(match.group('quantity'))
        total_price = price_each * quantity

        item_data["volume_deals_price"] = round(total_price, 2)
        item_data["unit_price"] = round(price_each, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Process '$X price each with Y' type promotions for coupons."""
        item_data = item.copy()
        price_each = float(match.group('price'))
        quantity = int(match.group('quantity'))
        # unit_price = round((item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)) - (price_each / quantity), 2)
        # item_data["unit_price"] = round(unit_price)
        # item_data["digital_coupon_price"] = round(price_each)

        # import pdb; pdb.set_trace()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        unit_price = round(price -(price_each / quantity), 2)
        # unit_price = round(price -(price_each / quantity), 2)
        digital_coupon_price = price_each * quantity

        item_data["unit_price"] = round(digital_coupon_price/2, 2)
        item_data["digital_coupon_price"] = round(digital_coupon_price,2)
        return item_data


class PriceEachWithQuantityProcessorNEW(PromoProcessor, version=2):
    """Processor for handling '$X price each with Y' type promotions."""

    # patterns = [r'\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+each\s+(?:when\s+you\s+buy|with|for)\s+(?P<quantity>\d+)',
    # r'\$(?P<price>\d+(?:\.\d{2})?)\s*ea\.?\s*(?:when\s+you\s+buy|when\s+buy)\s+(?P<quantity>\d+)\s+or\s+more'
    # ]
    patterns = [
    r'\$(?P<price>\d+(?:\.\d{2})?)\s*ea\.?\s*(?:when\s+you\s+buy|when\s+buy)\s+(?P<quantity>\d+)\s+or\s+more',
    r'\$(?P<price>\d+(?:\.\d{2})?)\s*(?:each|ea\.?)\s*(?:when\s+you\s+buy|with|for)\s+(?P<quantity>\d+)'
    ]




    def calculate_deal(self, item, match):
        """Process '$X price each with Y' type promotions for deals."""
        item_data = item.copy()
        price_each = float(match.group('price'))
        quantity = int(match.group('quantity'))
        total_price = price_each * quantity

        item_data["volume_deals_price"] = round(total_price, 2)
        item_data["unit_price"] = round(price_each, 2)
        # item_data["volume_deals_price"] = round(price_each, 2)
        # item_data["unit_price"] = round(price_each/quantity, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Process '$X price each with Y' type promotions for coupons."""
        item_data = item.copy()
        price_each = float(match.group('price'))
        quantity = int(match.group('quantity'))
        # unit_price = round((item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)) - (price_each / quantity), 2)
        # item_data["unit_price"] = round(unit_price)
        # item_data["digital_coupon_price"] = round(price_each)

        # import pdb; pdb.set_trace()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        unit_price = round(price -(price_each / quantity), 2)
        # unit_price = round(price -(price_each / quantity), 2)
        digital_coupon_price = price_each * quantity

        item_data["unit_price"] = round(digital_coupon_price/2, 2)
        item_data["digital_coupon_price"] = round(digital_coupon_price,2)
        return item_data

from promo_processor.processor import PromoProcessor

class WordBasedQuantityPriceProcessor(PromoProcessor):
    patterns = [
        # r"\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+When\s+you\s+buy\s+(?P<quantity>\w+)",
        # r"\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+When\s+you\s+buy\s+[any]?\s?+(?P<quantity>\w+)\s+\(\d+\)",
        r"(?P<count>\d+)/\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+when\s+you\s+buy\s+(?P<quantity>\w+)\s+\(\d+\)\s+or\s+more"
    ]
    def calculate_deal(self, item, match):
        """Calculate promotion price for '$X When you buy ONE' type promotions."""
        item_data = item.copy()
        volume_deals_price = float(match.group('volume_deals_price'))
        quantity_word = match.group('quantity')
        quantity = self.NUMBER_MAPPING.get(quantity_word.upper(), 1)
        unit_price = volume_deals_price / quantity
        
        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data



    def calculate_coupon(self, item, match):
        """Calculate promotion price for '$X When you buy ONE' type promotions."""
        item_data = item.copy()
        volume_deals_price = float(match.group('volume_deals_price'))
        quantity_word = match.group('quantity')
        quantity = self.NUMBER_MAPPING.get(quantity_word.upper(), 1)
        unit_price = volume_deals_price / quantity
        
        item_data["digital_coupon_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        return item_data
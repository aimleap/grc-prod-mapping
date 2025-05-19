from promo_processor import PromoProcessor

class AddTotalForOffer(PromoProcessor, version=1):
    """Processor for 'Add 2 Total For Offer' type promotions."""

    patterns = [r"(?i)\bAdd\s*(?P<quantity>\d+)\s*Total\s*For\s*Offer\b"]
    def calculate_deal(self, item, match):
        item_data = item.copy()
        price = item_data.get('sale_price') or item_data.get('regular_price')

        quantity = float(match.group('quantity'))
        price_for_quantity = price / quantity
        volume_deals_price = price
        unit_price = price_for_quantity

        item_data["volume_deals_price"] = round(volume_deals_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        item_data = item.copy()
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        savings_value = float(match.group('savings'))

        quantity = float(match.group('quantity'))
        price_for_quantity = price / quantity
        volume_deals_price = price
        unit_price = price_for_quantity

        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round(savings_value, 2)
        return item_data

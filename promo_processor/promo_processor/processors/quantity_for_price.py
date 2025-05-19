from promo_processor.processor import PromoProcessor

class QuantityForPriceProcessor(PromoProcessor, version=1):
    patterns = [
        # r"(?P<quantity>\d+)\s+For\s+\$(?P<volume_deals_price>\d+(?:\.\d+)?)",
        # r"Buy\s+(?P<quantity>\d+)\s+for\s+\$(?P<volume_deals_price>\d+(?:\.\d+)?)",
        r"(?P<volume_deals_price>\d+(?:¢|c))\s+each\s+when\s+you\s+buy\s+(?P<quantity>\d+)",
        # r"\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+when\s+you\s+buy\s+(?P<quantity>\d+)",
        r"^\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+when\s+you\s+buy\s+(?P<quantity>\d+)",

    ]

    def calculate_deal(self, item, match):
        """Calculate promotion price for 'X for $Y' promotions."""

        item_data = item.copy()
        quantity = int(match.group('quantity'))
        if "¢" in item.get('volume_deals_description'):
            cents = float(match.group('volume_deals_price').replace("¢",''))
            volume_deals_price = f"{cents / 100:.2f}"
            volume_deals_price = float(volume_deals_price)
            volume_deals_price_ = volume_deals_price*quantity
        elif "save up to" in item.get('volume_deals_description').lower():
            volume_deals_price = float(match.group('volume_deals_price'))
            volume_deals_price_ = volume_deals_price
        else:
            volume_deals_price = float(match.group('volume_deals_price'))
            volume_deals_price_ = volume_deals_price*quantity
        item_data["volume_deals_price"] = round(volume_deals_price_, 2)
        item_data["unit_price"] = round(volume_deals_price_ / quantity, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount."""
        item_data = item.copy()
        quantity = int(match.group('quantity'))
        volume_deals_price = float(match.group('volume_deals_price'))
        item_data["unit_price"] = round(volume_deals_price / quantity, 2)
        item_data["digital_coupon_price"] = round(volume_deals_price, 2)
        return item_data


class QuantityForPriceProcessorfor(PromoProcessor, version=2):
    patterns = [
        r"(?P<quantity>\d+)\s+For\s+\$(?P<volume_deals_price>\d+(?:\.\d+)?)",
        r"Buy\s+(?P<quantity>\d+)\s+for\s+\$(?P<volume_deals_price>\d+(?:\.\d+)?)",
    ]

    def calculate_deal(self, item, match):
        """Calculate promotion price for 'X for $Y' promotions."""

        item_data = item.copy()
        quantity = int(match.group('quantity'))
        volume_deals_price = float(match.group('volume_deals_price'))
        volume_deals_price_ = volume_deals_price
        item_data["volume_deals_price"] = round(volume_deals_price_, 2)
        item_data["unit_price"] = round(volume_deals_price_ / quantity, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount."""
        item_data = item.copy()
        quantity = int(match.group('quantity'))
        volume_deals_price = float(match.group('volume_deals_price'))
        item_data["unit_price"] = round(volume_deals_price / quantity, 2)
        item_data["digital_coupon_price"] = round(volume_deals_price, 2)
        return item_data

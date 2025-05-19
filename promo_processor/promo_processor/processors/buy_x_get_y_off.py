from promo_processor.processor import PromoProcessor


class BuyGetDiscountProcessor(PromoProcessor):
    patterns = [
        r"Buy\s+(?P<quantity>\d+)\s+get\s+(?P<discount>\d+)%\s+off\b",
        r"Buy\s+(?P<buy>\d+)\s+Get\s+(?P<get>\d+)\s+(?P<discount>\d+)%\s+Off\b",
        # "(?i)buy\s*(\d+)[\.,]?\s*get\s*(\d+)\s*(\d+)%\soff\sselect\sbeloved\spersonal\scare\sitems" #"Buy 1. get 1 50% off select Beloved personal care items"
        "(?i)buy\s*(?P<buy>\d+)[\.,]?\s*get\s*(?P<get>\d+)\s*(?P<discount>\d+)%\soff\sselect\sbeloved\spersonal\scare\sitems"


    ]

    #"Buy 2 get 50% off"
    #"Buy 1 Get 1 50% Off"

    def calculate_deal(self, item, match):
        """Calculate promotion price for 'Buy X get Y% off' promotions."""

        item_data = item.copy()
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)

        if "buy" in match.groupdict() and "get" in match.groupdict():
            buy_quantity = int(match.group('buy'))
            get_quantity = int(match.group('get'))
            discount_percentage = int(match.group('discount'))
            total_quantity = buy_quantity + get_quantity

            full_price_items = buy_quantity * price
            discounted_items = get_quantity * (price * (1 - discount_percentage / 100))
            volume_deals_price = full_price_items + discounted_items
            unit_price = volume_deals_price / total_quantity
        else:
            quantity = int(match.group('quantity'))
            discount_percentage = int(match.group('discount'))
            volume_deals_price = (price * quantity) - ((price * quantity) * (discount_percentage / 100))
            unit_price = volume_deals_price / quantity

        item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0

        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the final price after applying a coupon discount."""

        item_data = item.copy()
        price = item_data.get("unit_price") or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        if "buy" in match.groupdict() and "get" in match.groupdict():
            buy_quantity = int(match.group('buy'))
            get_quantity = int(match.group('get'))
            discount_percentage = int(match.group('discount'))
            total_quantity = buy_quantity + get_quantity

            full_price_items = buy_quantity * price
            discounted_items = get_quantity * (price * (1 - discount_percentage / 100))
            volume_deals_price = full_price_items + discounted_items

            unit_price = volume_deals_price / total_quantity
            # digital_coupon_price = (price * total_quantity) - discounted_items
        else:
            quantity = int(match.group('quantity'))
            discount_percentage = int(match.group('discount'))
            volume_deals_price = (price * quantity) - ((price * quantity) * (discount_percentage / 100))
            unit_price = volume_deals_price / quantity

        item_data['digital_coupon_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price, 2)

        return item_data



# (price * quantity)-discount

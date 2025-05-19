from promo_processor.processor import PromoProcessor

class CouponDiscountProcessor(PromoProcessor):
    patterns = [
        r"(?:Coupon):\s+\$?(?P<discount>\d+(?:\.\d+)?)\s+(?:off|%)",
    ]


    def calculate_deal(self, item, match):
        """Process 'Coupon: $X off' type promotions."""
        item_data = item.copy()
        discount = float(match.group('discount'))
        price = item_data.get("promo_price", item_data.get("regular_price", 0))
        volume_deals_price = price - discount

        item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(volume_deals_price / 1, 2)
        item_data['digital_coupon_price'] = ""

        return item_data

    def calculate_coupon(self, item, match):
        """Process coupon discount calculation."""

        item_data = item.copy()
        discount = float(match.group('discount'))
        price = item_data.get("unit_price") or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        volume_deals_price = price - discount

        # weight_val = float(item.get('weight').split()[0]) if item.get('weight').lower().endswith("oz") else item.get('weight')
        # try:
        #     unit_price = round(price / weight_val, 2)
        # except:
        #     weight_val = float(weight_val.split(" ")[0])
        #     unit_price = round(price / weight_val, 2)


        item_data['digital_coupon_price'] = round(volume_deals_price, 2)
        # item_data['unit_price'] = round(unit_price , 2)
        if volume_deals_price < 0:
            item_data['unit_price'] = 0
        else:
            item_data['unit_price'] = round(volume_deals_price / 1, 2)
        return item_data

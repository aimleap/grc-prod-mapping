from promo_processor.processor import PromoProcessor
import re
class BuyGetFreeProcessor(PromoProcessor, version=1):
    patterns = [
        r"Buy\s+(?P<quantity>\d+)\s+save\s+(?P<discount>\d+)%\s+off\b",
    ]

    def calculate_deal(self, item, match):
        """Process 'Buy X Save Y% off' specific promotions."""
        item_data = item.copy()
        quantity = int(match.group('quantity'))
        discount = int(match.group('discount'))

        price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        volume_deals_price = price * quantity
        per_discount_price = volume_deals_price * (discount/100)
        price_after_discount = volume_deals_price - per_discount_price

        unit_price = price_after_discount / quantity
        # total_quantity = quantity + free
        #
        # price = float(price) if price else 0
        # volume_deals_price = price * quantity
        # unit_price = price_per_item_after_volume_deal / total_quantity

        item_data['unit_price'] = round(unit_price, 2)
        item_data['volume_deals_price'] = round(price_after_discount, 2)
        item_data['digital_coupon_price'] = 0


        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for 'Buy X Save Y% off' promotions."""
        item_data = item.copy()

        quantity = int(match.group('quantity'))
        discount = int(match.group('discount'))

        price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        volume_deals_price = price * quantity
        per_discount_price = volume_deals_price * (discount/100)
        price_after_discount = volume_deals_price - per_discount_price

        unit_price = price_after_discount / quantity
        # total_quantity = quantity + free
        #
        # price = float(price) if price else 0
        # volume_deals_price = price * quantity
        # unit_price = price_per_item_after_volume_deal / total_quantity

        item_data['unit_price'] = round(unit_price, 2)
        item_data['volume_deals_price'] = round(price_after_discount, 2)
        item_data['digital_coupon_price'] = 0

        return item_data


class BuyGetDiscountProcessor(PromoProcessor, version=2):
    patterns = [
        r"Buy\s+(?P<quantity>\d+),\s+get\s+(?P<free>\d+)\s+(?P<discount>\d+)%\s+off"
    ]

    def calculate_deal(self, item, match):
        """Process 'Buy X Get Y % off' specific promotions."""
        item_data = item.copy()

        quantity = int(match.group('quantity'))
        free = int(match.group('free'))
        discount = int(match.group('discount'))
        price = item_data.get('sale_price') or item_data.get('regular_price', 0)
        total_quantity = quantity + free

        total_price = price * total_quantity
        discount_amount = total_price * (1 - discount / 100)
        unit_price = (total_price - discount_amount) / total_quantity

        item_data['volume_deals_price'] = round(discount_amount, 2)
        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = 0

        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for 'Buy X Get Y % off' promotions."""
        item_data = item.copy()

        quantity = int(match.group('quantity'))
        free = int(match.group('free'))
        discount = int(match.group('discount'))
        price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        total_quantity = quantity + free

        total_price = price * total_quantity
        discount_amount = total_price * (1 - discount / 100)
        unit_price = (total_price - discount_amount) / total_quantity

        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = round(discount_amount, 2)

        return item_data

class BuyOneGetOneFreeProcessor(PromoProcessor, version=3):
    patterns = [
        r"Get 1 Free When Buy 1 Get"
    ]

    def calculate_deal(self, item, match):
        """Process 'Buy 1 Get ONE(1) Free' specific promotions."""
        item_data = item.copy()
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        # Calculate unit price (assuming per item cost)
        unit_price = base_price
         # Check for digital coupon (BOGO deals)
        digital_coupon_price = base_price  # Default to base price
        if "Buy 1 Get ONE(1) Free" in item_data.get('digital_coupon_description'):
            digital_coupon_price = base_price / 2  # BOGO means each costs half when buying two
        # Check for volume deals
        volume_deals_price = base_price  # Default to base price
        match = re.search(r'(\d+) for \$(\d+\.\d+)', item_data.get('volume_deals_description'))
        if match:
            qty = int(match.group(1))
            total_price = float(match.group(2))
            volume_deals_price = total_price / qty  # Price per item in volume deal

        item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = 0
        # item_data['digital_coupon_price'] = round(digital_coupon_price,2)

        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount for 'Buy X Get Y Free' promotions."""
        item_data = item.copy()

        """Process 'Buy 1 Get ONE(1) Free' specific promotions."""
        item_data = item.copy()
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        # Calculate unit price (assuming per item cost)
        unit_price = base_price
         # Check for digital coupon (BOGO deals)
        digital_coupon_price = base_price  # Default to base price
        if "Buy 1 Get ONE(1) Free" in item_data.get('digital_coupon_description'):
            digital_coupon_price = base_price / 2  # BOGO means each costs half when buying two
        # Check for volume deals
        volume_deals_price = base_price  # Default to base price
        match = re.search(r'(\d+) for \$(\d+\.\d+)', item_data.get('volume_deals_description'))
        if match:
            qty = int(match.group(1))
            total_price = float(match.group(2))
            volume_deals_price = total_price / qty  # Price per item in volume deal

        # item_data['volume_deals_price'] = 0
        # item_data['volume_deals_price'] = round(volume_deals_price, 2)
        item_data['unit_price'] = round(unit_price, 2)
        item_data['digital_coupon_price'] = round(digital_coupon_price,2)


        return item_data

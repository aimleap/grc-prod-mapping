from promo_processor.processor import PromoProcessor
import re

class BasicPricePerLbProcessor(PromoProcessor, version=1):
    """Processor for handling basic '$X/lb' promotions."""

    patterns = [
        r'\$(?P<price_per_lb>\d+(?:\.\d{2})?)\/lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\/lb'
    ]

    def calculate_deal(self, item, match):
        """Process basic '$X/lb' type promotions for deals."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        if isinstance(item_data.get('weight', 0), str):
            weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            total_price = price_per_lb * weight
            item_data["volume_deals_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(price_per_lb, 2)
            item_data["digital_coupon_price"] = 0

        return item_data

    def calculate_coupon(self, item, match):
        """Process basic '$X/lb' type promotions for coupons."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        unit_price = float(item_data.get('unit_price', 0) or 0)
        if isinstance(item_data.get('weight', 0), str):
            weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            coupon_savings = price_per_lb * weight
            item_data["digital_coupon_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(price_per_lb, 2)

        return item_data

class SaveUpToPricePerLbProcessor(PromoProcessor, version=2):
    """Processor for handling '$X/lb with Save Up To' promotions."""

    patterns = [
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+\.\d{2})\s+Lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+(?:\.\d{1,2})?)\s+Lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+(?:\.\d{1,2})?)'
    ]

    def calculate_deal(self, item, match):
        """Process '$X/lb with Save Up To' type promotions for deals."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        if isinstance(item_data.get('weight'), str):
            if len(item_data.get('weight')) > 1 and any(i for i in item_data.get('weight') if  i.isdigit()):
                weight = float("".join([i for i in item_data.get('weight') if i.isdigit() or i == "."]))
            else:
                weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            total_price = price_per_lb / weight
            item_data["volume_deals_price"] = round(total_price, 2)
            item_data["unit_price"] = round(price_per_lb * weight, 2)
            item_data["digital_coupon_price"] = 0

            savings_per_lb = float(match.group('savings'))
            item_data["volume_deals_price"] = round(savings_per_lb * weight, 2)
        else:
            item_data["volume_deals_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(price_per_lb, 2)
            item_data["digital_coupon_price"] = 0


        return item_data

    def calculate_coupon(self, item, match):
        """Process '$X/lb with Save Up To' type promotions for coupons."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        if isinstance(item_data.get('weight', 0), str):
            weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)

        if weight:
            weight = float(weight)
            savings_per_lb = float(match.group('savings'))
            coupon_savings = savings_per_lb * weight
            item_data["digital_coupon_price"] = round(price_per_lb, 2)
            if item_data['unit_price']:
                item_data["unit_price"] = round(item_data['unit_price'] - coupon_savings, 2)
            else:
                item_data['unit_price'] = ""

        return item_data

class PricePerLbProcessor(PromoProcessor, version=3):
    """Processor for handling basic '$X per lb.' promotions."""

    patterns = [
        # r'\$([\d\.]+) per lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\s*per\s*lb\.?\s*Limit\s+(?P<limit_lbs>\d+)-?lbs?',
        r'\$(?P<price_per_lb>[\d\.]+)\s*per\s*lb'


    ]

    def calculate_deal(self, item, match):
        """Process basic '$X per lb.' type promotions for deals."""
        item_data = item.copy()
        price_per_lb = float(match.group('price_per_lb'))
        if isinstance(item_data.get('weight', 0), str):
            weight = 1
        else:
            weight = float(item_data.get('weight', 0) or 1)
        if weight:
            weight = float(weight)
            total_price = price_per_lb * weight
            item_data["volume_deals_price"] = round(price_per_lb, 2)
            item_data["unit_price"] = round(price_per_lb, 2)
            item_data["digital_coupon_price"] = 0

        return item_data

    def calculate_coupon(self, item, match):
        """Process basic '$X per lb.' type promotions for coupons."""
        item_data = item.copy()
    # Parse weight (assume format like '2.000 LB')
        price_per_lb = float(match.group('price_per_lb'))
        try:
            limit_lbs = float(match.group('limit_lbs'))
        except:
            limit_lbs = 1

        weight_val = 0
        if "approx" not in str(item_data.get('weight')).lower():
            weight_val = float(item_data.get('weight').split()[0])

        # Determine base price (sale price if available, otherwise regular price)
        # base_price = float(sale_price) if sale_price else float(regular_price)
        base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        # Calculate unit price (price per pound or per unit)
        try:
            unit_price = round(base_price / weight_val, 2)
        except:
            unit_price = 0

        # Digital coupon price
        digital_coupon_price = base_price
        match_coupon = re.search(r'\$([\d\.]+) per lb', item_data.get('digital_coupon_description'))
        if match_coupon:
            per_lb_price = float(match_coupon.group(1))
            digital_coupon_price = round(per_lb_price * weight_val, 2)

        # # Volume deal price (if any)
        # volume_deals_price = base_price  # Default to base
        # match_volume = re.search(r'(\\d+) for \\$(\\d+\\.\\d+)', item_data.get('volume_deals_description'))
        # if match_volume:
        #     qty = int(match_volume.group(1))
        #     total_price = float(match_volume.group(2))
        #     volume_deals_price = round(total_price / qty, 2)
        item_data["unit_price"] =  round(digital_coupon_price, 2)
        item_data["digital_coupon_price"] =  round(digital_coupon_price, 2)
        # item_data["volume_deals_price"] =  round(volume_deals_price, 2)
        return item_data

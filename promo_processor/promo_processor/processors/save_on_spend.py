from promo_processor.processor import PromoProcessor

class SpendSaveProcessor(PromoProcessor, version=1):
    patterns = [
        r'Spend\s+\$(?P<spend>\d+(?:\.\d{2})?)\s+Save\s+\$(?P<savings>\d+(?:\.\d{2})?)\s+on\s+.*?',
    ]

    def calculate_deal(self, item, match):
        """Calculate the volume deals price for a deal."""
        item_data = item.copy()
        savings_value = float(match.group('savings'))
        spend_requirement = float(match.group('spend'))
        price = item_data.get('sale_price') or item_data.get('regular_price', 0)

        discount_rate = savings_value / spend_requirement
        unit_price = price - (price * discount_rate)

        item_data["volume_deals_price"] = round(unit_price, 2)
        item_data["unit_price"] = round(unit_price / 1, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount."""
        item_data = item.copy()
        savings_value = float(match.group('savings'))
        spend_requirement = float(match.group('spend'))
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        discount_rate = savings_value / spend_requirement
        unit_price = price - (price * discount_rate)

        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round((savings_value), 2)
        return item_data

class OffWhenSpendProcessor(PromoProcessor, version=2):
    patterns = [
        r'\$(?P<savings>\d+(?:\.\d{2})?)\s+off\s+When\s+you\s+spend\s+\$(?P<spend>\d+(?:\.\d{2})?)\s+on\s+.*?',
        r'\$(?P<savings>\d+(?:\.\d{2})?)\s+off\s+When\s+you\s+spend\s+\$(?P<spend>\d+)',
    ]

    def calculate_deal(self, item, match):
        """Calculate the volume deals price for a deal."""
        item_data = item.copy()
        savings_value = float(match.group('savings'))
        spend_requirement = float(match.group('spend'))
        price = item_data.get('sale_price') or item_data.get('regular_price', 0)

        discount_rate = savings_value / spend_requirement
        unit_price = price - (price * discount_rate)

        item_data["volume_deals_price"] = round(unit_price, 2)
        item_data["unit_price"] = round(unit_price / 1, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount."""
        item_data = item.copy()
        savings_value = float(match.group('savings'))
        spend_requirement = float(match.group('spend'))
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        discount_rate = savings_value / spend_requirement
        unit_price = price - (price * discount_rate)

        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round((savings_value), 2)
        return item_data

class SaveWhenSpendProcessor(PromoProcessor, version=3):

    patterns = [
        # r'Save\s+\$(?P<savings>\d+(?:\.\d{2})?)\s+When\s+You\s+Spend\s+\$(?P<spend>\d+(?:\.\d{2})?)',
        r'Get\s+(?P<percent>\d+)%\s+off\s+When\s+you\s+spend\s+\$(?P<spend>\d+(?:\.\d{2})?)',
        # r'\$(?P<savings>\d+)\s+Target\s+GiftCard\s+with\s+select\s+\$(?P<spend>\d+(?:\.\d{2})?)\s+skin\s+care\s+purchase',
        # r'\$(?P<savings>\d+)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+\$(?P<spend>\d+)(?:\s+[\w\s&]+\s+purchase)?'
    ]
    def calculate_deal(self, item, match):
        """Calculate the volume deals price for a deal."""
        item_data = item.copy()
        spend_requirement = float(match.group('spend'))
        price = item_data.get('sale_price') or item_data.get('regular_price', 0)

        if "percent" in match.groupdict():
            percent = float(match.group('percent'))
            discount_rate = percent / 100
        else:
            savings_value = float(match.group('savings'))
            discount_rate = savings_value / spend_requirement

        unit_price = price - (price * discount_rate)

        item_data["volume_deals_price"] = round(spend_requirement, 2)
        item_data["unit_price"] = round(unit_price / 1, 2)
        item_data["digital_coupon_price"] = 0
        return item_data

    def calculate_coupon(self, item, match):
        """Calculate the price after applying a coupon discount."""
        item_data = item.copy()
        spend_requirement = float(match.group('spend'))
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

        if "percent" in match.groupdict():
            percent = float(match.group('percent'))
            discount_rate = percent / 100
            savings_value = price * discount_rate
        else:
            savings_value = float(match.group('savings'))
            discount_rate = savings_value / spend_requirement

        unit_price = price - (price * discount_rate)

        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round((spend_requirement), 2)
        return item_data


#
# class SaveWhenSpendProcessor2(PromoProcessor, version=4):
#
#     patterns = [
#         r'Save\s+\$(?P<savings>\d+(?:\.\d{2})?)\s+When\s+You\s+Spend\s+\$(?P<spend>\d+(?:\.\d{2})?)',
#         r'\$(?P<savings>\d+)\s+Target\s+GiftCard\s+with\s+select\s+\$(?P<spend>\d+(?:\.\d{2})?)\s+skin\s+care\s+purchase',
#         r'\$(?P<savings>\d+)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+\$(?P<spend>\d+)(?:\s+[\w\s&]+\s+purchase)?'
#     ]
#     def calculate_deal(self, item, match):
#         """Calculate the volume deals price for a deal."""
#         item_data = item.copy()
#         spend_requirement = float(match.group('spend'))
#         price = item_data.get('sale_price') or item_data.get('regular_price', 0)
#
#         item_data["volume_deals_price"] = 0
#         item_data["unit_price"] = 0
#         item_data["digital_coupon_price"] = 0
#         return item_data
#
#     def calculate_coupon(self, item, match):
#         """Calculate the price after applying a coupon discount."""
#         item_data = item.copy()
#         spend_requirement = float(match.group('spend'))
#         price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
#         item_data["unit_price"] = price
#         item_data["digital_coupon_price"] = 0
#         return item_data

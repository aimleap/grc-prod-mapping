from promo_processor.processor import PromoProcessor

class GiftCardProcessor(PromoProcessor, version=1):
    """Processor for handling gift card promotions."""

    patterns = [
        r'\$(?P<amount>\d+(?:\.\d+)?)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+(?P<quantity>\d+)\s+select\s+(?P<category>[\w\s&]+)'
    ]

    def calculate_deal(self, item, match):
        """Process gift card promotions for deals."""
    
        item_data = item.copy()
        quantity = int(match.group('quantity'))
        discount = float(match.group('amount'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        total_price = price * quantity
        discounted_price = total_price - discount
        unit_price = discounted_price / quantity
        item_data["volume_deals_price"] = round(discount, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
    
    def calculate_coupon(self, item, match):
        """Process gift card promotions for coupons."""
        item_data = item.copy()
        quantity = int(match.group('quantity'))
        discount = float(match.group('amount'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        total_price = price * quantity
        discounted_price = total_price - discount
        unit_price = discounted_price / quantity
        
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = discount
        return item_data

class GiftCardPurchaseProcessor(PromoProcessor, version=2):
    """Processor for handling gift card promotions with purchase amount."""

    patterns = [
        r'\$(?P<amount>\d+(?:\.\d+)?)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+\$(?P<purchase>\d+(?:\.\d+)?)\s+select\s+(?P<category>[\w\s&]+)\s+purchase'
    ]

    def calculate_deal(self, item, match):
        """Process gift card promotions for deals."""
    
        item_data = item.copy()
        spend_requirement = float(match.group('purchase'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        discount_value = float(match.group('amount'))
        discount_rate = discount_value / spend_requirement
        
        unit_price = price - (price * discount_rate)
        
        item_data["volume_deals_price"] = round(unit_price, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
    
    def calculate_coupon(self, item, match):
        """Process gift card promotions for coupons."""
        item_data = item.copy()
        spend_requirement = float(match.group('purchase'))
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        discount_value = float(match.group('amount'))
        discount_rate = discount_value / spend_requirement
        savings_value = price * discount_rate
        
        unit_price = price - (price * discount_rate)
        
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round(savings_value, 2)
        return item_data


class SimpleGiftCardProcessor(PromoProcessor, version=3):
    """Processor for handling simple gift card promotions."""

    patterns = [
        r'\$(?P<amount>\d+)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+(?P<purchase>\d+)\s+(?P<item>[\w\s]+)'
    ]
    def calculate_deal(self, item, match):
        """Process simple gift card promotions for deals."""
        item_data = item.copy()
        quantity = float(match.group('purchase'))
        price = item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        discount_value = float(match.group('amount'))
        discount = (price * quantity) - discount_value
        unit_price = discount / quantity
        
        item_data["volume_deals_price"] = round(discount, 2)
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = 0
        return item_data
    
    def calculate_coupon(self, item, match):
        """Process simple gift card promotions for coupons."""
        item_data = item.copy()
        quantity = float(match.group('purchase'))
        price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
        
        discount_value = float(match.group('amount'))
        discount = (price * quantity) - discount_value
        unit_price = discount / quantity
        
        item_data["unit_price"] = round(unit_price, 2)
        item_data["digital_coupon_price"] = round(discount, 2)
        return item_data




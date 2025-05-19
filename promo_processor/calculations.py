about_each_price

AboutEachPriceProcessor:
patterns = [r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s+limit\s+(?P<min_quantity>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+each.\s+limit\s+(?P<quantity>\d+)\s+.*?limit\s+(?P<min_quantity>\d+)",
                r"\$(?P<unit_price>\d+(?:\.\d+)?)\s+Each"]

Example: "$5.99 Each" or "$2.50 Each"
calculate_deal

unit_price = float(match.group('unit_price'))
quantity = item_data.get("quantity", 1)
volume_deals_price = unit_price * quantity
unit_price_calculated = volume_deals_price / quantity

item_data['volume_deals_price'] = round(volume_deals_price, 2)
item_data['unit_price'] = round(unit_price_calculated, 2)
item_data['digital_coupon_price'] = 0

calculate_coupon
unit_price = float(match.group('unit_price'))
quantity = item_data.get("quantity", 1)
volume_deals_price = unit_price * quantity
unit_price_calculated = volume_deals_price / quantity

item_data['digital_coupon_price'] = round(unit_price_calculated, 2)
item_data["unit_price"] = round(unit_price_calculated, 2)

________________________________________________________________________________

SaveEachWhenBuyMoreProcessor:
patterns = [r"Save\s+\$(?P<discount>\d+(?:\.\d+)?)\s+each\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)\s+or\s+more"]
# Save $1 each when you buy 5 or more
calculate_deal
discount = float(match.group('discount'))
min_quantity = int(match.group('min_quantity'))
quantity = item_data.get("quantity", 1)
original_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

volume_deals_price = discount * min_quantity
unit_price = ((original_price * min_quantity) - volume_deals_price) / min_quantity
volume_deals_priceNew = (original_price * min_quantity) - volume_deals_price

item_data['volume_deals_price'] = round(volume_deals_priceNew, 2)
if unit_price < 0:
    item_data['unit_price'] = ""
else:
    item_data['unit_price'] = round(unit_price, 2)
item_data['digital_coupon_price'] = 0


calculate_coupon
discount = float(match.group('discount'))
min_quantity = int(match.group('min_quantity'))
quantity = item_data.get("quantity", 1)
original_price = item_data.get("unit_price", 0)

if quantity >= min_quantity:
    discounted_price = original_price - discount
    item_data['digital_coupon_price'] = round(discounted_price, 2)
    item_data["unit_price"] = round(discounted_price, 2)
################################################################################


buy_x_get_y_off

BuyGetDiscountProcessor:
patterns = [
        r"Buy\s+(?P<quantity>\d+)\s+get\s+(?P<discount>\d+)%\s+off\b",
        r"Buy\s+(?P<buy>\d+)\s+Get\s+(?P<get>\d+)\s+(?P<discount>\d+)%\s+Off\b",
    ]

#"Buy 2 get 50% off"
#"Buy 1 Get 1 50% Off"
calculate_deal
"""Calculate promotion price for 'Buy X get Y% off' promotions."""
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

calculate_coupon
"""Calculate the final price after applying a coupon discount."""
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
else:
    quantity = int(match.group('quantity'))
    discount_percentage = int(match.group('discount'))
    volume_deals_price = (price * quantity) - ((price * quantity) * (discount_percentage / 100))
    unit_price = volume_deals_price / quantity

item_data['digital_coupon_price'] = round(volume_deals_price, 2)
item_data['unit_price'] = round(unit_price, 2)


################################################################################
buy_x_get_y
BuyGetFreeProcessor:
patterns = [
        r"Buy\s+(?P<quantity>\d+),?\s+Get\s+(?P<free>\d+)\s+Free"
    ]
calculate_deal
"""Process 'Buy X Get Y Free' specific promotions."""
quantity = int(match.group('quantity'))
free = int(match.group('free'))
price = item_data.get('regular_price', 0)
total_quantity = quantity + free
volume_deals_price = price * quantity
unit_price = volume_deals_price / total_quantity if total_quantity > 0 else 1

item_data['volume_deals_price'] = round(volume_deals_price, 2)
item_data['unit_price'] = round(unit_price, 2)
item_data['digital_coupon_price'] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount for 'Buy X Get Y Free' promotions."""
quantity = int(match.group('quantity'))
free = int(match.group('free'))
price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

total_quantity = quantity + free
price = float(price) if price else 0
volume_deals_price = price * quantity
unit_price = volume_deals_price / total_quantity

item_data['unit_price'] = round(unit_price, 2)
item_data['digital_coupon_price'] = round(volume_deals_price, 2)

________________________________________________________________________________

BuyGetDiscountProcessor:
patterns = [
        r"Buy\s+(?P<quantity>\d+),\s+get\s+(?P<free>\d+)\s+(?P<discount>\d+)%\s+off"]
calculate_deal
"""Process 'Buy X Get Y % off' specific promotions."""

""" old logic
quantity = int(match.group('quantity'))
free = int(match.group('free'))
discount = int(match.group('discount'))
price = item_data.get('sale_price') or item_data.get('regular_price', 0)
total_quantity = quantity + free

total_price = price * total_quantity
discount_amount = total_price * (1 - discount / 100)
unit_price = (total_price - discount_amount) / total_quantity
"""

buy_qty = int(match.group('quantity'))
get_qty = int(match.group('free'))
discount = int(match.group('discount'))
price_per_item = item_data.get('sale_price') or item_data.get('regular_price', 0)

discount_amount = price_per_item * (1 - discount / 100)
total_items = buy_qty + get_qty
total_price = (buy_qty * price_per_item) + (get_qty * discount_amount)
unit_price = total_price / total_items
discountperc = (discount / 100)
volume_deals_price = price_per_item * buy_qty + (price_per_item - (price_per_item * discountperc))
# volume_deals_price = price_per_item + discount_amount
item_data['volume_deals_price'] = round(volume_deals_price, 2)
item_data['unit_price'] = round(unit_price, 2)
item_data['digital_coupon_price'] = 0

calculate_coupon
"""Calculate the price after applying a coupon discount for 'Buy X Get Y % off' promotions."""
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

________________________________________________________________________________

BuyOneGetOneFreeProcessor:
patterns = [r"Get 1 Free When Buy 1 Get"]
calculate_deal
"""Process 'Buy 1 Get ONE(1) Free' specific promotions."""

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

calculate_coupon
"""Calculate the price after applying a coupon discount for 'Buy X Get Y Free' promotions."""


"""Process 'Buy 1 Get ONE(1) Free' specific promotions."""

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



################################################################################
buy_x_save_x
BuyGetFreeProcessor:
patterns = [
        r"Buy\s+(?P<quantity>\d+)\s+save\s+(?P<discount>\d+)%\s+off\b",]

calculate_deal
"""Process 'Buy X Save Y% off' specific promotions."""

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




calculate_coupon
"""Calculate the price after applying a coupon discount for 'Buy X Save Y% off' promotions."""


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

________________________________________________________________________________



BuyGetDiscountProcessor:
patterns = [
        r"Buy\s+(?P<quantity>\d+),\s+get\s+(?P<free>\d+)\s+(?P<discount>\d+)%\s+off"]

calculate_deal
"""Process 'Buy X Get Y % off' specific promotions."""


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



calculate_coupon
"""Calculate the price after applying a coupon discount for 'Buy X Get Y % off' promotions."""


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


________________________________________________________________________________

BuyOneGetOneFreeProcessor:
patterns = [
        r"Get 1 Free When Buy 1 Get"
    ]
calculate_deal
"""Process 'Buy 1 Get ONE(1) Free' specific promotions."""

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



calculate_coupon
"""Calculate the price after applying a coupon discount for 'Buy X Get Y Free' promotions."""


"""Process 'Buy 1 Get ONE(1) Free' specific promotions."""

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



################################################################################
coupon_discount
CouponDiscountProcessor
patterns = [
        r"(?:Coupon):\s+\$?(?P<discount>\d+(?:\.\d+)?)\s+(?:off|%)",
    ]


calculate_deal
"""Process 'Coupon: $X off' type promotions."""

discount = float(match.group('discount'))
price = item_data.get("promo_price", item_data.get("regular_price", 0))
volume_deals_price = price - discount

item_data['volume_deals_price'] = round(volume_deals_price, 2)
item_data['unit_price'] = round(volume_deals_price / 1, 2)
item_data['digital_coupon_price'] = ""



calculate_coupon
"""Process coupon discount calculation."""


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

################################################################################
deals

TargetCircleDealProcessor
"Processor for Target Circle Deals"""

patterns = [
            r"Target Circle Deal\s*:\s*\$(\d+\.?\d*)\s+price\s+on\s+select\s+(.+)"
        ]
    # Example: "Target Circle Deal: $10.99 price on select items"
calculate_deal
"""Calculate the final price after applying a coupon discount."""

select_price = float(match.group(1))

item_data['volume_deals_price'] = round(select_price, 2)
item_data['unit_price'] = round(select_price, 2)
item_data['digital_coupon_price'] = ""


calculate_coupon

select_price = float(match.group(1))

item_data['volume_deals_price'] = round(select_price, 2)
item_data['unit_price'] = round(select_price, 2)
item_data['digital_coupon_price'] = ""


###############################################################################
dollor_discount



DollarDiscountProcessor:
"""Processor for handling '$X off' type promotions."""

patterns = [
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off'
    ]

calculate_deal
"""Process '$X off' type promotions for deals."""


discount_value = float(match.group('discount'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
volume_deals_price = price - discount_value

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(volume_deals_price, 2)
item_data["digital_coupon_price"] = 0
item_data["quantity"] = 1


calculate_coupon
"""Process '$X off' type promotions for coupons."""

discount_value = float(match.group('discount'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
unit_price = price - discount_value
if unit_price < 0 :
    item_data["unit_price"] = ""
else:
    item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount_value, 2)
item_data["quantity"] = 1

________________________________________________________________________________

DollarDiscountQuantityProcessor:
"""Processor for handling '$X off when buy Y' type promotions."""

patterns = [
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off\s+when\s+buy\s+(?P<quantity>\d+)(?:\s+limit\s+(?P<limit>\d+))?'
    ]

calculate_deal
"""Process '$X off when buy Y' type promotions for deals."""


discount_value = float(match.group('discount'))
quantity = int(match.group('quantity'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
volume_deals_price = (price * quantity - discount_value) / quantity

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(volume_deals_price, 2)
item_data["digital_coupon_price"] = 0
item_data["quantity"] = quantity


calculate_coupon
"""Process '$X off when buy Y' type promotions for coupons."""

discount_value = float(match.group('discount'))
quantity = int(match.group('quantity'))
limit = int(match.group('limit')) if 'limit' in match.groupdict() else quantity
price = item_data.get("sale_price") or item_data.get("regular_price", 0)

# if limit > quantity:
#     unit_price = (price * limit) - (discount_value / quantity)
# else:
unit_price = price - (discount_value / quantity)

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount_value / quantity, 2)
item_data["quantity"] = quantity
________________________________________________________________________________


DollarDiscountLimitProcessor:
"""Processor for handling '$X off limit Y' type promotions."""

patterns = [
        r'\$(?P<discount>\d+(?:\.\d+)?)\s+off\s+limit\s+(?P<limit>\d+)'
    ]

calculate_deal
"""Process '$X off limit Y' type promotions for deals."""


discount_value = float(match.group('discount'))
limit = int(match.group('limit'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
volume_deals_price = price - (discount_value / limit)

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(volume_deals_price, 2)
item_data["digital_coupon_price"] = 0
item_data["quantity"] = limit


calculate_coupon
"""Process '$X off limit Y' type promotions for coupons."""

discount_value = float(match.group('discount'))
limit = int(match.group('limit'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
unit_price = price - (discount_value / limit)

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount_value / limit, 2)
item_data["quantity"] = limit
________________________________________________________________________________


BuyNGetMDiscountProcessor:
"""Processor for handling 'Buy N Get M $X Off' type promotions."""

patterns = [
        r'Buy\s+(?P<buy>\d+)\s+Get\s+(?P<get>\d+)\s+\$(?P<discount>\d+(?:\.\d+)?)\s+Off'
    ]

calculate_deal
"""Process 'Buy N Get M $X Off' type promotions for deals."""


buy_quantity = int(match.group('buy'))
get_quantity = int(match.group('get'))
discount_value = float(match.group('discount'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
total_quantity = buy_quantity + get_quantity
volume_deals_price = (price * total_quantity - discount_value) / total_quantity

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(volume_deals_price, 2)
item_data["digital_coupon_price"] = 0
item_data["quantity"] = total_quantity


calculate_coupon
"""Process 'Buy N Get M $X Off' type promotions for coupons."""

buy_quantity = int(match.group('buy'))
get_quantity = int(match.group('get'))
discount_value = float(match.group('discount'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
total_quantity = buy_quantity + get_quantity
unit_price = price - (discount_value / total_quantity)

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount_value / total_quantity, 2)
item_data["quantity"] = total_quantity

################################################################################
fixed_price_meal_processor
from typing import Dict, Any


BasicFixedPriceProcessor:
patterns = [
        r'^\$(?P<price>\d+\.?\d*)$',
        r'^\$(?P<price>\d+\.?\d*)\s+price\s',
        r'^(?P<price>\d+)¢',
    ]

    def calculate_deal(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:

        price = float(match.group('price'))

        if "¢" in item_data["volume_deals_description"]:
            price = float(match.group('price')) / 100

        item_data["volume_deals_price"] = round(price, 2)
        item_data["unit_price"] = round(price, 2)
        item_data["digital_coupon_price"] = 0
        item_data["required_quantity"] = 1
        item_data["limit"] = 0



    def calculate_coupon(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:

        price = float(match.group('price'))
        if "¢" in item_data["digital_coupon_description"]:
            price = float(match.group('price')) / 100

        item_data["digital_coupon_price"] = round(price, 2)
        item_data["unit_price"] = round(price, 2)
        item_data["required_quantity"] = 1
        item_data["limit"] = 0



LimitedFixedPriceProcessor:
patterns = [
        r'^\$(?P<price>\d+\.?\d*)\s+When\s+Buy\s+(?P<quantity>\d+)\s+Limit\s+(?P<limit>\d+)',
    ]

    def calculate_deal(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:

        price = float(match.group('price'))
        quantity = int(match.group('quantity'))

        item_data["volume_deals_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        item_data["required_quantity"] = quantity
        item_data["limit"] = int(match.group('limit'))



    def calculate_coupon(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:

        price = float(match.group('price'))
        quantity = int(match.group('quantity'))

        item_data["digital_coupon_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["required_quantity"] = quantity
        item_data["limit"] = int(match.group('limit'))

________________________________________________________________________________


MultiQuantityFixedPriceProcessor:
patterns = [
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)\s+or\s+more',
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+Mix\s*&\s*Match\s+multiples\s+of\s+(?P<min_quantity>\d+)',
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)',
        r'^.*(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+when\s+you\s+buy\s+(?P<min_quantity>\d+)',
        r'^(?P<quantity>\d+)/\$(?P<price>\d+\.?\d*)\s+must\s+buy\s+(?P<min_quantity>\d+)\s+or\s+more',
    ]

    def calculate_deal(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:

        price = float(match.group('price'))
        quantity = int(match.group('quantity'))
        min_quantity = int(match.group('min_quantity'))

        if min_quantity > quantity:
            quantity = min_quantity

        item_data["volume_deals_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["digital_coupon_price"] = 0
        item_data["required_quantity"] = quantity
        item_data["limit"] = 0



    def calculate_coupon(self, item: Dict[str, Any], match: re.Match) -> Dict[str, Any]:

        price = float(match.group('price'))
        quantity = int(match.group('quantity'))
        min_quantity = int(match.group('min_quantity'))

        if min_quantity > quantity:
            quantity = min_quantity

        item_data["digital_coupon_price"] = round(price, 2)
        item_data["unit_price"] = round(price / quantity, 2)
        item_data["required_quantity"] = quantity
        item_data["limit"] = 0



################################################################################
giftcard
GiftCardProcessor:
"""Processor for handling gift card promotions."""

patterns = [
        r'\$(?P<amount>\d+(?:\.\d+)?)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+(?P<quantity>\d+)\s+select\s+(?P<category>[\w\s&]+)'
    ]

calculate_deal
"""Process gift card promotions for deals."""
quantity = int(match.group('quantity'))
discount = float(match.group('amount'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
total_price = price * quantity
discounted_price = total_price - discount
unit_price = discounted_price / quantity
item_data["volume_deals_price"] = round(discount, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Process gift card promotions for coupons."""

quantity = int(match.group('quantity'))
discount = float(match.group('amount'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)
total_price = price * quantity
discounted_price = total_price - discount
unit_price = discounted_price / quantity

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = discount
________________________________________________________________________________


GiftCardPurchaseProcessor:
"""Processor for handling gift card promotions with purchase amount."""

patterns = [
        r'\$(?P<amount>\d+(?:\.\d+)?)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+\$(?P<purchase>\d+(?:\.\d+)?)\s+select\s+(?P<category>[\w\s&]+)\s+purchase'
    ]

calculate_deal
"""Process gift card promotions for deals."""


spend_requirement = float(match.group('purchase'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)

discount_value = float(match.group('amount'))
discount_rate = discount_value / spend_requirement

unit_price = price - (price * discount_rate)

item_data["volume_deals_price"] = round(unit_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Process gift card promotions for coupons."""

spend_requirement = float(match.group('purchase'))
price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

discount_value = float(match.group('amount'))
discount_rate = discount_value / spend_requirement
savings_value = price * discount_rate

unit_price = price - (price * discount_rate)

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(savings_value, 2)

________________________________________________________________________________


SimpleGiftCardProcessor:
"""Processor for handling simple gift card promotions."""

patterns = [
        r'\$(?P<amount>\d+)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+(?P<purchase>\d+)\s+(?P<item>[\w\s]+)'
    ]
calculate_deal
"""Process simple gift card promotions for deals."""

quantity = float(match.group('purchase'))
price = item_data.get("sale_price") or item_data.get("regular_price", 0)

discount_value = float(match.group('amount'))
discount = (price * quantity) - discount_value
unit_price = discount / quantity

item_data["volume_deals_price"] = round(discount, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Process simple gift card promotions for coupons."""

quantity = float(match.group('purchase'))
price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

discount_value = float(match.group('amount'))
discount = (price * quantity) - discount_value
unit_price = discount / quantity

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount, 2)

###############################################################################
Offer
AddTotalForOffer:
"""Processor for 'Add 2 Total For Offer' type promotions."""

patterns = [r"(?i)\bAdd\s*(?P<quantity>\d+)\s*Total\s*For\s*Offer\b"]
calculate_deal

price = item_data.get('sale_price') or item_data.get('regular_price')

quantity = float(match.group('quantity'))
price_for_quantity = price / quantity
volume_deals_price = price
unit_price = price_for_quantity

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
savings_value = float(match.group('savings'))

quantity = float(match.group('quantity'))
price_for_quantity = price / quantity
volume_deals_price = price
unit_price = price_for_quantity

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(savings_value, 2)

###############################################################################
percentage_discount


PercentageOffProcessor:
patterns = [
        r"^(?P<discount>\d+)%\s+off",
        r"^(?P<discount>\d+)%\s+of",
        r"^(?P<discount>\d+)%\s+select",
        r"^Deal:\s+(?P<discount>\d+)%\s+off",
        r"^Save\s+(?P<discount>\d+)%$",
        r"^Save\s+(?P<discount>\d+)%\s+on",
        r"^Save\s+(?P<discount>\d+)%",

    ]

calculate_deal

discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
price = item_data.get("sale_price") or item_data.get('regular_price', 0)
price = float(price) if price else 0

discounted_price = price * (1 - discount_decimal)
unit_price = discounted_price

item_data["volume_deals_price"] = round(discounted_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
base_price = float(base_price) if base_price else 0
discounted_price = base_price * (1 - discount_decimal)

item_data["unit_price"] = round(discounted_price, 2)
item_data["digital_coupon_price"] = round(discounted_price, 2)

________________________________________________________________________________

PercentageOffProductProcessor:
patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+on\s+(?P<product>[\w\s-]+)",
        r"^Save\s+(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
        r"^(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s-]+)",
    ]

calculate_deal

discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
price = item_data.get("sale_price") or item_data.get('regular_price', 0)
price = float(price) if price else 0

discounted_price = price * (1 - discount_decimal)
unit_price = discounted_price

item_data["volume_deals_price"] = round(discounted_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

""" old logic
discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
base_price = float(base_price) if base_price else 0

discounted_price = base_price * (1 - discount_decimal)
item_data["unit_price"] = round(discounted_price, 2)
item_data["digital_coupon_price"] = round(discounted_price, 2)
"""
base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
base_price = float(base_price) if base_price else 0

discount_percent = float(match.group('discount'))
discount_amount = round(base_price * (discount_percent / 100), 2)
final_price = round(base_price - discount_amount, 2)

item_data["unit_price"] = round(final_price, 2)
item_data["digital_coupon_price"] = round(discount_amount, 2)

________________________________________________________________________________

PercentageOffQuantityProcessor:
patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+with\s+(?P<quantity>\d+)",
        r"^Save\s+(?P<discount>\d+)%\s+each\s+when\s+you\s+buy\s+(?P<quantity>\d+)\s+or\s+more",
    ]

calculate_deal

discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
price = item_data.get("sale_price") or item_data.get('regular_price', 0)
price = float(price) if price else 0

quantity = int(match.group('quantity'))
if "or more" in match.string:
    item_data["min_quantity"] = quantity
    discounted_price = price * (1 - discount_decimal)
    unit_price = discounted_price
else:
    total_price = price * quantity
    discounted_price = total_price * (1 - discount_decimal)
    unit_price = discounted_price / quantity

item_data["volume_deals_price"] = round(discounted_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
base_price = float(base_price) if base_price else 0

discounted_price = base_price * (1 - discount_decimal)

item_data["unit_price"] = round(discounted_price, 2)
item_data["digital_coupon_price"] = round(discounted_price, 2)

________________________________________________________________________________


PercentageOffSelectProcessor:
patterns = [
        r"^Save\s+(?P<discount>\d+)%\s+select",
    ]

calculate_deal

discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
price = item_data.get("sale_price") or item_data.get('regular_price', 0)
price = float(price) if price else 0

discounted_price = price * (1 - discount_decimal)

item_data["volume_deals_price"] = round(discounted_price, 2)
item_data["unit_price"] = round(discounted_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

discount_percentage = float(match.group('discount'))
discount_decimal = discount_percentage / 100
base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
base_price = float(base_price) if base_price else 0

discounted_price = base_price * (1 - discount_decimal)

item_data["unit_price"] = round(discounted_price, 2)
item_data["digital_coupon_price"] = round(discounted_price, 2)


###############################################################################

price_each_with_quantity


PriceEachWithQuantityProcessor
"""Processor for handling '$X price each with Y' type promotions."""

patterns = [r'\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+each\s+(?:when\s+you\s+buy|with|for)\s+(?P<quantity>\d+)']



calculate_deal
"""Process '$X price each with Y' type promotions for deals."""

price_each = float(match.group('price'))
quantity = int(match.group('quantity'))
total_price = price_each * quantity

item_data["volume_deals_price"] = round(total_price, 2)
item_data["unit_price"] = round(price_each, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Process '$X price each with Y' type promotions for coupons."""

price_each = float(match.group('price'))
quantity = int(match.group('quantity'))
unit_price = round((item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)) - (price_each / quantity), 2)

item_data["unit_price"] = round(unit_price)
item_data["digital_coupon_price"] = round(price_each)



###############################################################################
price_per_lb
BasicPricePerLbProcessor:
    """Processor for handling basic '$X/lb' promotions."""

patterns = [
        r'\$(?P<price_per_lb>\d+(?:\.\d{2})?)\/lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\/lb'
    ]

calculate_deal
"""Process basic '$X/lb' type promotions for deals."""

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



calculate_coupon
"""Process basic '$X/lb' type promotions for coupons."""

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

________________________________________________________________________________


SaveUpToPricePerLbProcessor:
    """Processor for handling '$X/lb with Save Up To' promotions."""

patterns = [
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+\.\d{2})\s+Lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+(?:\.\d{1,2})?)\s+Lb',
        r'\$(?P<price_per_lb>\d+\.\d{2})\s+Lb\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+(?:\.\d{1,2})?)'
    ]

calculate_deal
"""Process '$X/lb with Save Up To' type promotions for deals."""

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




calculate_coupon
"""Process '$X/lb with Save Up To' type promotions for coupons."""

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

________________________________________________________________________________


PricePerLbProcessor:
    """Processor for handling basic '$X per lb.' promotions."""

patterns = [
        r'\$([\d\.]+) per lb'
    ]

calculate_deal
"""Process basic '$X per lb.' type promotions for deals."""

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



calculate_coupon
"""Process basic '$X per lb.' type promotions for coupons."""
# Parse weight (assume format like '2.000 LB')
weight_val = float(item_data.get('weight').split()[0])

# Determine base price (sale price if available, otherwise regular price)
# base_price = float(sale_price) if sale_price else float(regular_price)
base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

# Calculate unit price (price per pound or per unit)
unit_price = round(base_price / weight_val, 2)

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

item_data["unit_price"] =  round(unit_price, 2)
item_data["digital_coupon_price"] =  round(digital_coupon_price, 2)
# item_data["volume_deals_price"] =  round(volume_deals_price, 2)


###############################################################################
quantity_for_price


QuantityForPriceProcessor
patterns = [
        r"(?P<quantity>\d+)\s+For\s+\$(?P<volume_deals_price>\d+(?:\.\d+)?)",
        r"Buy\s+(?P<quantity>\d+)\s+for\s+\$(?P<volume_deals_price>\d+(?:\.\d+)?)"
    ]


calculate_deal
"""Calculate promotion price for 'X for $Y' promotions."""


quantity = int(match.group('quantity'))
volume_deals_price = float(match.group('volume_deals_price'))

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(volume_deals_price / quantity, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount."""

quantity = int(match.group('quantity'))
volume_deals_price = float(match.group('volume_deals_price'))

item_data["unit_price"] = round(volume_deals_price / quantity, 2)
item_data["digital_coupon_price"] = round(volume_deals_price, 2)

###############################################################################
save_on_quantity



SaveOnQuantityTotalProcessor:
patterns = [
        r"\$(?P<total_price>\d+(?:\.\d+)?)\s+SAVE\s+\$(?P<discount>\d+(?:\.\d+)?)\s+on\s+(?P<quantity>\w+)\s+\(\d+\)",
    ]

calculate_deal
"""Process '$X SAVE $Y on Z' type promotions."""

try:
    total_price = float(match.group('total_price'))
except IndexError:
    total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))

discount = float(match.group('discount'))
quantity = float(match.group('quantity'))

volume_deals_price = (total_price * quantity) - discount

item_data["volume_deals_price"] = round(discount, 2)
item_data["unit_price"] = round(volume_deals_price / quantity, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount for Save $X on Y promotions."""

unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
if isinstance(unit_price, str) and not unit_price:
    unit_price = 0

quantity = float(match.group('quantity'))
discount = float(match.group('discount'))

total_price = (unit_price * quantity) - discount
unit_price = total_price / quantity if quantity > 0 else 0

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount, 2)

________________________________________________________________________________


SaveOnQuantityProductProcessor:
patterns = [
        r"(?i)SAVE\s+\$(?P<discount>\d+(?:\.\d+)?)\s+on\s+(?P<quantity>\d+)\s+(?P<product>[\w\s-]+)",
    ]

calculate_deal
"""Process '$X SAVE $Y on Z' type promotions."""

try:
    total_price = float(match.group('total_price'))
except IndexError:
    total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))

discount = float(match.group('discount'))
quantity = float(match.group('quantity'))

volume_deals_price = (total_price * quantity) - discount

item_data["volume_deals_price"] = round(discount, 2)
item_data["unit_price"] = round(volume_deals_price / quantity, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount for Save $X on Y promotions."""

unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
if isinstance(unit_price, str) and not unit_price:
    unit_price = 0

quantity = float(match.group('quantity'))
discount = float(match.group('discount'))

total_price = (unit_price * quantity) - discount
unit_price = total_price / quantity if quantity > 0 else 0

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount, 2)

________________________________________________________________________________


SaveOnQuantityLimitProcessor:
patterns = [
        r"\$(?P<discount>\d+(?:\.\d+)?)\s+OFF\s+When\s+Buy\s+(?P<quantity>\d+)(?:\s+Limit\s+(?P<limit>\d+))?",
    ]

calculate_deal
"""Process '$X SAVE $Y on Z' type promotions."""

try:
    total_price = float(match.group('total_price'))
except IndexError:
    total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))

discount = float(match.group('discount'))
quantity = float(match.group('quantity'))

volume_deals_price = (total_price * quantity) - discount

item_data["volume_deals_price"] = round(discount, 2)
item_data["unit_price"] = round(volume_deals_price / quantity, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount for Save $X on Y promotions."""

unit_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
if isinstance(unit_price, str) and not unit_price:
    unit_price = 0

quantity = float(match.group('quantity'))
discount = float(match.group('discount'))

total_price = (unit_price * quantity) - discount
unit_price = total_price / quantity if quantity > 0 else 0

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount, 2)


________________________________________________________________________________

SaveOnQuantitySimpleProcessor:
patterns = [
        r"Save\s+\$(?P<discount>\d+(?:\.\d+)?)\s+on\s+(?P<quantity>\d+)",
        r"Save\s+\$(?P<discount>\d+(?:\.\d+)?)\s+when\s+you\s+buy\s+(?P<quantity>\d+)",
        r"Buy\s+(?P<quantity>\d+),\s+Save\s+\$(?P<discount>\d+(?:\.\d+)?)",
    ]

calculate_deal
"""Process '$X SAVE $Y on Z' type promotions."""

try:
    total_price = float(match.group('total_price'))
except IndexError:
    total_price = float(item_data.get("sale_price") or item_data.get("regular_price", 0))

discount = float(match.group('discount'))
quantity = float(match.group('quantity'))

volume_deals_price = (total_price * quantity) - discount

item_data["volume_deals_price"] = round(discount, 2)
item_data["unit_price"] = round(volume_deals_price / quantity, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount for Save $X on Y promotions."""

price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
if isinstance(price, str) and not price:
    price = 0
quantity = float(match.group('quantity'))
discount = float(match.group('discount'))

total_price = (price * quantity) - discount
unit_price = total_price / quantity if quantity > 0 else 0
if unit_price < 0:
    item_data["unit_price"] = ""
else:
    item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(discount, 2)


###############################################################################
save_on_spend


SpendSaveProcessor:
patterns = [
        r'Spend\s+\$(?P<spend>\d+(?:\.\d{2})?)\s+Save\s+\$(?P<savings>\d+(?:\.\d{2})?)\s+on\s+.*?',
    ]

calculate_deal
"""Calculate the volume deals price for a deal."""

savings_value = float(match.group('savings'))
spend_requirement = float(match.group('spend'))
price = item_data.get('sale_price') or item_data.get('regular_price', 0)

discount_rate = savings_value / spend_requirement
unit_price = price - (price * discount_rate)

item_data["volume_deals_price"] = round(unit_price, 2)
item_data["unit_price"] = round(unit_price / 1, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount."""

savings_value = float(match.group('savings'))
spend_requirement = float(match.group('spend'))
price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

discount_rate = savings_value / spend_requirement
unit_price = price - (price * discount_rate)

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round((savings_value), 2)
________________________________________________________________________________


OffWhenSpendProcessor:
patterns = [
        r'\$(?P<savings>\d+(?:\.\d{2})?)\s+off\s+When\s+you\s+spend\s+\$(?P<spend>\d+(?:\.\d{2})?)\s+on\s+.*?',
        r'\$(?P<savings>\d+(?:\.\d{2})?)\s+off\s+When\s+you\s+spend\s+\$(?P<spend>\d+)',
    ]

calculate_deal
"""Calculate the volume deals price for a deal."""

savings_value = float(match.group('savings'))
spend_requirement = float(match.group('spend'))
price = item_data.get('sale_price') or item_data.get('regular_price', 0)

discount_rate = savings_value / spend_requirement
unit_price = price - (price * discount_rate)

item_data["volume_deals_price"] = round(unit_price, 2)
item_data["unit_price"] = round(unit_price / 1, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Calculate the price after applying a coupon discount."""

savings_value = float(match.group('savings'))
spend_requirement = float(match.group('spend'))
price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

discount_rate = savings_value / spend_requirement
unit_price = price - (price * discount_rate)

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round((savings_value), 2)
________________________________________________________________________________


SaveWhenSpendProcessor:

patterns = [
        r'Save\s+\$(?P<savings>\d+(?:\.\d{2})?)\s+When\s+You\s+Spend\s+\$(?P<spend>\d+(?:\.\d{2})?)',
        r'Get\s+(?P<percent>\d+)%\s+off\s+When\s+you\s+spend\s+\$(?P<spend>\d+(?:\.\d{2})?)',
        r'\$(?P<savings>\d+)\s+Target\s+GiftCard\s+with\s+select\s+\$(?P<spend>\d+(?:\.\d{2})?)\s+skin\s+care\s+purchase',
        r'\$(?P<savings>\d+)\s+(?P<store>[\w\s]+)\s+GiftCard\s+with\s+\$(?P<spend>\d+)(?:\s+[\w\s&]+\s+purchase)?'
    ]
calculate_deal
"""Calculate the volume deals price for a deal."""

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


calculate_coupon
"""Calculate the price after applying a coupon discount."""

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

###############################################################################
savings


DollarOffProcessor:
patterns = [
        r'^Save\s+\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<quantity>\d+)\s+',  # Matches "Save $3.00 off 10 ..."
        r'^Save\s+\$(?P<savings>\d+(?:\.\d{2})?)',  # Matches "Save $3.00" or "Save $3"
        r'^\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<size>\d+\.?\d*-\d+\.?\d*-[a-zA-Z]+\.?)',  # Matches "$0.50 off  15.4-21-oz."
        r'^\$(?P<savings>\d+\.\d{2})\s+off\s+(?P<size>\d+\.?\d*-[a-zA-Z]+\.?)',  # Matches "$0.25 off 15.25-oz."
        r'^\$(?P<savings>\d+)\s+Target\s+GiftCard\s+on\s+Crest\s+teeth-whitening\s+strips',  # Matches "$5 Target GiftCard on Crest teeth-whitening strips"
        r'^\$(?P<savings>\d+)\s+Target\s+GiftCard\s+with\s+purchase',  # Matches "$20 Target GiftCard with purchase"
    ]
calculate_deal

price = item_data.get('sale_price') or item_data.get('regular_price')
savings_value = float(match.group('savings'))

quantity = 1
if 'quantity' in match.groupdict() and match.group('quantity'):
    quantity = float(match.group('quantity'))
    price_for_quantity = price * quantity
    savings_value_for_quantity = price_for_quantity - savings_value
    volume_deals_price = price
    unit_price = savings_value_for_quantity / quantity
else:
    volume_deals_price = price - savings_value
    unit_price = volume_deals_price

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
savings_value = float(match.group('savings'))

quantity = 1
if 'quantity' in match.groupdict() and match.group('quantity'):
    quantity = float(match.group('quantity'))
    price_for_quantity = price * quantity
    savings_value_for_quantity = price_for_quantity - savings_value
    volume_deals_price = price
    unit_price = savings_value_for_quantity / quantity
else:
    volume_deals_price = price - savings_value
    unit_price = volume_deals_price
if unit_price < 0:
    item_data["unit_price"] = ""
else:
    item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(savings_value, 2)

________________________________________________________________________________

CentsOffProcessor:
patterns = [
        r'^Save\s+\$(?P<savings>\.25)\s+',  # Matches "Save $.25 "
        r'^Save\s+(?P<savings>\d+)¢'  # Matches "Save 70¢"
    ]

calculate_deal

price = item_data.get('sale_price') or item_data.get('regular_price')

savings_value = float(match.group('savings'))
if "¢" in item_data["volume_deals_description"]:
    savings_value = savings_value / 100

volume_deals_price = price - savings_value
unit_price = volume_deals_price

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

savings_value = float(match.group('savings'))
if "¢" in item_data["digital_coupon_description"]:
    savings_value = savings_value / 100

volume_deals_price = price - savings_value
unit_price = volume_deals_price

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(savings_value, 2)
________________________________________________________________________________


PercentOffProcessor:
patterns = [
        r'^Save\s+(?P<percent>\d+)%\s+Off'  # Matches "Save 20% Off"
    ]

calculate_deal

price = item_data.get('sale_price') or item_data.get('regular_price')

percent = float(match.group('percent'))
savings_value = price * (percent / 100)

volume_deals_price = price - savings_value
unit_price = volume_deals_price

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

percent = float(match.group('percent'))
savings_value = price * (percent / 100)

volume_deals_price = price - savings_value
unit_price = volume_deals_price

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(savings_value, 2)
________________________________________________________________________________


PayPalRebateProcessor:
patterns = [
        r"\$(?P<rebate>\d+\.\d{2})\s+REBATE\s+via\s+PayPal\s+when\s+you\s+buy\s+(?P<quantity>ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)\s*(?:\(\d+\))?",
        r"Rebate:\s+\$(?P<rebate>\d+)\s+back\s+when\s+you\s+buy\s+(?P<quantity>\d+)"    ]

calculate_deal

rebate_amount = float(match.group('rebate'))
quantity = self.NUMBER_MAPPING[match.group('quantity').upper()] if match.group('quantity').isalpha() else float(match.group('quantity'))
price = item_data.get("sale_price") or item_data.get('regular_price', 0)
price = float(price) if price else 0

discounted_price = price - (rebate_amount / quantity)
unit_price = discounted_price

item_data["volume_deals_price"] = round(discounted_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0
item_data["rebate_amount"] = rebate_amount
item_data["rebate_type"] = "PayPal"


calculate_coupon

rebate_amount = float(match.group('rebate'))
quantity = self.NUMBER_MAPPING[match.group('quantity').upper()] if match.group('quantity').isalpha() else float(match.group('quantity'))
base_price = item_data.get('unit_price') or item_data.get("sale_price") or item_data.get("regular_price", 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
base_price = float(base_price) if base_price else 0

discounted_price = base_price - (rebate_amount / quantity)

item_data["unit_price"] = round(discounted_price, 2)
item_data["digital_coupon_price"] = round(rebate_amount / quantity, 2)
item_data["rebate_amount"] = rebate_amount
item_data["rebate_type"] = "PayPal"

________________________________________________________________________________

WinePackProcessor:
patterns = [
        r'^Wine\s+(?P<percent>\d+)%\s+(?P<quantity>\d+)\s+Pack\s+\$(?P<price>\d+\.\d{2})\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+\.\d{1})'
    ]

calculate_deal

percent = float(match.group('percent'))
quantity = float(match.group('quantity'))
pack_price = float(match.group('price'))
savings = float(match.group('savings'))

unit_price = pack_price / quantity
volume_deals_price = pack_price

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

percent = float(match.group('percent'))
quantity = float(match.group('quantity'))
pack_price = float(match.group('price'))
savings = float(match.group('savings'))

unit_price = pack_price / quantity

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(pack_price, 2)
________________________________________________________________________________


HealthyAislesProcessor:
patterns = [
        r'^Healthy\s+Aisles\s+\$(?P<price>\d+\.\d{2})\s+Save\s+Up\s+To:\s+\$(?P<savings>\d+\.\d{1})'
    ]

calculate_deal

price = float(match.group('price'))
savings = float(match.group('savings'))

volume_deals_price = price
unit_price = price

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon

price = float(match.group('price'))
savings = float(match.group('savings'))

unit_price = price

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(savings, 2)


###############################################################################
select_deal


SelectDealProcessor
patterns = [
        r"Deal:\s+\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+on\s+"
    ]


calculate_deal
"""Process 'Deal: $X price on select' type promotions."""

select_price = float(match.group('price'))

item_data["volume_deals_price"] = round(select_price, 2)
item_data["unit_price"] = round(select_price, 2)
item_data["digital_coupon_price"] = 0



calculate_coupon
"""Calculate the price for 'Deal: $X price on select' promotions when a coupon is applied."""

select_price = float(match.group('price'))
unit_price = (item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)) - select_price

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(select_price, 2)


###############################################################################
select_product_price


SelectProductPriceProcessor
    """Processor for handling '$X price on select Product' type promotions."""

patterns = [r'\$(?P<price>\d+(?:\.\d{2})?)\s+price\s+on\s+select\s+(?P<product>[\w\s-]+)']


calculate_deal
"""Process '$X price on select Product' type promotions for deals."""

select_price = float(match.group('price'))
weight = item_data.get('weight', 1)

item_data["volume_deals_price"] = round(select_price, 2)
item_data["unit_price"] = round(select_price / 1, 2)
item_data["digital_coupon_price"] = 0


calculate_coupon
"""Process '$X price on select Product' type promotions for coupons."""

select_price = float(match.group('price'))
weight = item_data.get('weight', 1)

item_data["unit_price"] = round(select_price / 1, 2)
item_data["digital_coupon_price"] = round(select_price, 2)



###############################################################################
target_circle_deal


TargetCircleDealProcessor
patterns = [
        r'Target Circle Deal\s*:\s*Buy\s+(?P<buy_qty>\d+),\s*get\s+(?P<get_qty>\d+)\s+(?P<discount>\d+)%\s+off\s+select\s+(?P<product>[\w\s]+)',
    ]


calculate_deal:
        """No volume deals calculation needed for this case"""



calculate_coupon:
"""Calculate coupon price for buy X get Y Z% off deals"""

buy_qty = int(match.group('buy_qty'))
get_qty = int(match.group('get_qty'))
discount_percent = int(match.group('discount'))

base_price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)

base_price = float(base_price)

regular_total = base_price * (buy_qty + get_qty)
discount_amount = (base_price * get_qty) * (discount_percent / 100)
final_price = regular_total - discount_amount

unit_price = final_price / (buy_qty + get_qty)

item_data["digital_coupon_price"] = round(final_price, 2)
item_data["unit_price"] = round(unit_price, 2)


###############################################################################
target_circle_percent


TargetCirclePercentProcessor
patterns = [
        r'Target Circle Deal\s*:\s*(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s&,-]+)',
        r'Target Circle\s*:\s*(?P<discount>\d+)%\s+off\s+(?P<product>[\w\s&,-]+)',
        r'Target Circle Deal\s*:\s*Save\s+(?P<discount>\d+)%\s+on\s+(?P<product>[\w\s&,\'-]+)(?:\s*-\s*(?P<quantity>\d+)(?:pk|pks|pack|packs))?'
    ]

calculate_deal:
        """No volume deals calculation needed for this case"""



calculate_coupon:
"""Calculate coupon price for percent off deals"""

discount_percent = int(match.group('discount'))

base_price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
base_price = float(base_price)

discount_amount = base_price * (discount_percent / 100)
final_price = base_price - discount_amount

item_data["digital_coupon_price"] = round(discount_amount, 2)

item_data["unit_price"] = round(final_price, 2)


###############################################################################
target_circle_price


TargetCirclePriceProcessor
patterns = [
        r'Target Circle Deal\s*:\s*\$(?P<price>\d+\.?\d*)\s+price\s+on\s+(?P<product>[\w\s-]+)',
        r'Target Circle Coupon\s*:\s*\$(?P<amount>\d+\.?\d*)\s+off',
    ]

calculate_deal:
        """No volume deals calculation needed for this case"""



calculate_coupon:
"""Calculate coupon price for fixed price deals and amount off deals"""

if 'price' in match.groupdict():
    price = float(match.group('price'))
    item_data["digital_coupon_price"] = price
    item_data["unit_price"] = price

elif 'amount' in match.groupdict():
    amount_off = float(match.group('amount'))
    original_price = item_data.get('unit_price') or item_data.get('sale_price') or item_data.get('regular_price', 0) if item.get("many") else item_data.get("sale_price") or item_data.get("regular_price", 0)
    new_price = max(0, original_price - amount_off)
    item_data["digital_coupon_price"] = amount_off
    item_data["unit_price"] = round(new_price)


###############################################################################
weight_based_promo



WeightBasedPromoProcessor
patterns = [
        r"\$(?P<volume_deals_price>\d+(?:\.\d+)?)\/lb\s+When\s+you\s+buy\s+(?P<quantity>\w+)\s+\(\d+\)"
    ]

calculate_deal
"""Process '$X/lb When you buy Y (Z)' type promotions."""

volume_deals_price = float(match.group('volume_deals_price'))
quantity_word = match.group('quantity')
quantity = self._convert_word_to_number(quantity_word)
unit_price = volume_deals_price / quantity

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0



calculate_coupon
"""Calculate the price after applying a coupon discount for weight-based promotions."""

volume_deals_price = float(match.group('volume_deals_price'))
quantity_word = match.group('quantity')
quantity = self._convert_word_to_number(quantity_word)
unit_price = volume_deals_price / quantity

item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = round(volume_deals_price, 2)


    def _convert_word_to_number(self, word: str) -> int:
        """Convert word-based quantity (e.g., 'ONE') to its numeric value using number mapping."""
        return self.NUMBER_MAPPING.get(word.upper(), 1)
###############################################################################
word_based_quantity_price


WordBasedQuantityPriceProcessor
patterns = [
        # r"\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+When\s+you\s+buy\s+(?P<quantity>\w+)",
        # r"\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+When\s+you\s+buy\s+[any]?\s?+(?P<quantity>\w+)\s+\(\d+\)",
        r"(?P<count>\d+)/\$(?P<volume_deals_price>\d+(?:\.\d+)?)\s+when\s+you\s+buy\s+(?P<quantity>\w+)\s+\(\d+\)\s+or\s+more"
    ]
calculate_deal
"""Calculate promotion price for '$X When you buy ONE' type promotions."""

volume_deals_price = float(match.group('volume_deals_price'))
quantity_word = match.group('quantity')
quantity = self.NUMBER_MAPPING.get(quantity_word.upper(), 1)
unit_price = volume_deals_price / quantity

item_data["volume_deals_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)
item_data["digital_coupon_price"] = 0




calculate_coupon
"""Calculate promotion price for '$X When you buy ONE' type promotions."""

volume_deals_price = float(match.group('volume_deals_price'))
quantity_word = match.group('quantity')
quantity = self.NUMBER_MAPPING.get(quantity_word.upper(), 1)
unit_price = volume_deals_price / quantity

item_data["digital_coupon_price"] = round(volume_deals_price, 2)
item_data["unit_price"] = round(unit_price, 2)

###############################################################################

from decimal import Decimal

def get_discount_info(price: Decimal, amount: int, loyalty: False):
    """Calculates the discounted price, the amount of discount,
    and the discount rate for an item having a specific price and
    given the number of items to sell.
    The `price` parameter is the unit price for a single item.
    The `amount` parameter is the number of items to sell.
    The `loyalty` parameter sets loyalty customer pricing on (True) or
    off (False). The default is off (False).
    The return value is a triplet with the following items:
    - the price for a single item after discount.
    - the amount of discount for a single item.
    - the discount rate."""

    discount = 0
    rate = 1
    after_discount = None

    if (amount * price) >= 500 or loyalty:
        # 30 % off if the total price is 500 or more
        # or if this is a loyalty customer
        rate = Decimal(0.30)
    else:
        if amount <= 3:
            rate = Decimal(0) # no discount
        elif amount > 3 and amount <= 10:
            rate = Decimal(0.10) # 10% discount
        elif amount > 10 and amount <= 20:
            rate = Decimal(0.15) # 15% discount
        elif amount > 20:
            rate = Decimal(0.20) # 20% discount

    discount = rate * price
    after_discount = price - discount

    return (after_discount, discount, rate)

if __name__ == "__main__":
    """This is a very simple driver that allows you to play with
    this small program. You can change the constants (in UPPER_CASE)
    to see the effects on the output. Run the program with:
    python3 discount.py
    """

    UNIT_PRICE = Decimal(5.95)
    AMOUNT = 10
    LOYALTY = False

    discount_info = get_discount_info(UNIT_PRICE, AMOUNT, LOYALTY)
    print("{:d} items at unit price {:.2f} cost {:.2f} each with discount {:.2f} at rate {:.2f} (loyalty customer: {})".format(AMOUNT, UNIT_PRICE, discount_info[0], discount_info[1], discount_info[2], LOYALTY))

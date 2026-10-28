"""Price helpers."""

GST_RATE = 0.18


def add_tax(price, rate=GST_RATE):
    return round(price * (1 + rate), 2)


def apply_discount(price, percent):
    if not 0 <= percent <= 100:
        raise ValueError("percent must be between 0 and 100")
    return round(price * (1 - percent / 100), 2)


if __name__ == "__main__":
    # Runs only with: python 08_modules_and_venv/shopkit/pricing.py
    print("Running pricing.py directly. __name__ =", __name__)
    print("add_tax(100) =", add_tax(100))
    print("apply_discount(200, 10) =", apply_discount(200, 10))

"""Turn raw user input (always a str) into clean values.     [Topics 01, 02, 07]

Every function here either returns a valid value or raises an ExpenseError
with a message that tells the user how to fix their input. Keeping this
separate from input() makes it easy to test: no keyboard needed.
"""
import math
from datetime import date, datetime

from errors import ExpenseError, InvalidAmountError, InvalidCategoryError, InvalidDateError
from models import CATEGORIES

DATE_FORMAT = "%d-%m-%Y"  # 28-10-2026, the format people in India write dates in
MAX_AMOUNT = 10_000_000


def parse_amount(text: str) -> float:
    cleaned = text.strip().replace(",", "").removeprefix("₹").strip()
    try:
        amount = float(cleaned)
    except ValueError:
        # `from None` hides the technical ValueError; our message is clearer.
        raise InvalidAmountError(
            f'"{text.strip()}" is not a number. Enter an amount like 250 or 99.50'
        ) from None
    # float() also accepts "nan" and "inf", so check the number is a real one.
    if not math.isfinite(amount):
        raise InvalidAmountError("Enter a real amount, like 250 or 99.50")
    if amount <= 0:
        raise InvalidAmountError("Amount must be more than 0")
    if amount > MAX_AMOUNT:
        raise InvalidAmountError("That amount looks too large. Check it and try again")
    return round(amount, 2)


def parse_category(text: str) -> str:
    """Accept a category name ('food') or its number in the list ('1')."""
    choice = text.strip().lower()
    if choice.isdigit():
        number = int(choice)
        if 1 <= number <= len(CATEGORIES):
            return CATEGORIES[number - 1]
    elif choice in CATEGORIES:
        return choice
    raise InvalidCategoryError(
        f'"{text.strip()}" is not a category. Pick a name or number from the list'
    )


def parse_date(text: str, today: date) -> date:
    """Empty input means today. `today` is passed in so tests can control it."""
    text = text.strip()
    if not text:
        return today
    try:
        when = datetime.strptime(text, DATE_FORMAT).date()
    except ValueError:
        raise InvalidDateError(
            f'"{text}" is not a valid date. Use DD-MM-YYYY, like {today:%d-%m-%Y}'
        ) from None
    if when > today:
        raise InvalidDateError("The date can't be in the future")
    return when


def parse_id(text: str) -> int:
    text = text.strip()
    if not text.isdigit():
        raise ExpenseError(f'"{text}" is not an ID. Enter a number, like 3')
    return int(text)

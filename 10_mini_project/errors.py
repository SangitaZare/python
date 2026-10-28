"""Custom exceptions for the expense tracker.                       [Topic 07]

All of them inherit from ExpenseError, so the menu code can catch every
"the user typed something wrong" problem with one `except ExpenseError`,
while real bugs (TypeError, NameError...) still crash loudly.
"""


class ExpenseError(Exception):
    """Base class: a problem we can explain to the user."""


class InvalidAmountError(ExpenseError):
    """The amount is not a positive number."""


class InvalidCategoryError(ExpenseError):
    """The category is not in the allowed list."""


class InvalidDateError(ExpenseError):
    """The date is missing, badly formatted, or in the future."""


class ExpenseNotFoundError(ExpenseError):
    """No expense has the requested ID."""


class StorageError(ExpenseError):
    """The data file exists but cannot be read."""

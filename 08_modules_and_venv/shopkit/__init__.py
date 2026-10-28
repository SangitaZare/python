"""shopkit - a tiny demo package for topic 08.

This file runs once, when the package is first imported. It re-exports the
most useful functions so users can write `from shopkit import add_tax`
instead of `from shopkit.pricing import add_tax`.
"""
from .pricing import add_tax, apply_discount  # relative imports inside the package
from .text import slugify

__all__ = ["add_tax", "apply_discount", "slugify"]
__version__ = "1.0.0"

print(f"  [shopkit/__init__.py ran: package loaded, version {__version__}]")

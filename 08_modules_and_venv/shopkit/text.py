"""Text helpers."""
import re


def slugify(text):
    """'Blue Cotton T-Shirt!' -> 'blue-cotton-t-shirt'"""
    text = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return text.strip("-")

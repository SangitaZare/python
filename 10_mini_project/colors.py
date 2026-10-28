"""A tiny helper for coloured terminal text.                    [Topics 02, 08]

Terminals understand "ANSI escape codes": special text like \033[33m that
switches the colour (33 = yellow) and \033[0m that resets it. Libraries such
as `rich` and `colorama` do this for you, but it is only a few lines, and
writing it yourself shows there is no magic.
"""
import os
import sys

CODES = {
    "bold": "1",
    "dim": "2",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "magenta": "35",
    "cyan": "36",
    "bright_red": "91",
    "bright_yellow": "93",
    "bright_blue": "94",
    "white": "97",
}

CATEGORY_COLORS = {
    "bills": "bright_blue",
    "food": "bright_yellow",
    "shopping": "magenta",
    "transport": "cyan",
    "fun": "bright_red",
    "health": "green",
    "other": "white",
}

# Colours only make sense in a real terminal. When output is piped to a
# file they would show up as junk like "[33m", so switch them off.
# NO_COLOR is a common convention: https://no-color.org
ENABLED = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def enable_windows_ansi() -> None:
    """Older Windows consoles need this nudge before they show ANSI colours."""
    if ENABLED and os.name == "nt":
        os.system("")


def paint(text: str, *styles: str) -> str:
    if not ENABLED or not styles:
        return text
    codes = ";".join(CODES[style] for style in styles)
    return f"\033[{codes}m{text}\033[0m"


def category_color(category: str) -> str:
    return CATEGORY_COLORS.get(category, "white")

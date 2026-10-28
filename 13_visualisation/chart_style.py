"""One place for every chart's colours and styling.

Import it at the top of a notebook and call apply():

    import chart_style as cs
    cs.apply()

Why a module? If each chart picks its own colours, "Electronics" ends up blue
in one chart and green in the next, and readers get confused. Defining the
palette once keeps every chart consistent, and a change here updates them all.

The categorical colours were checked with a colour-blindness validator: the
four slots stay distinguishable for the common types of colour blindness.
Two of them (aqua, yellow) are light, so charts using them always add
direct labels or a legend, never colour alone.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

# ---- colours --------------------------------------------------------------

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"
AXIS = "#c3c2b7"

# Fixed categorical order. Assign slots in this order and never cycle past 8.
SLOTS = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100",
         "#e87ba4", "#008300", "#6250d6", "#e34948"]

# Colour follows the entity: a category is always the same colour, in every
# chart, even when a filter removes the others.
CATEGORY_COLORS = {
    "Electronics": SLOTS[0],
    "Clothing": SLOTS[1],
    "Books": SLOTS[2],
    "Home": SLOTS[3],
}

# The single colour for one-series charts.
PRIMARY = SLOTS[0]

# Sequential ramp (one hue, light -> dark) for magnitude, e.g. heatmaps.
BLUE_RAMP = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
BLUES = LinearSegmentedColormap.from_list("blues", BLUE_RAMP)

# Diverging (two opposite hues + a neutral grey middle) for values with a sign,
# like correlations from -1 to +1. The middle must read as "nothing".
DIVERGING = LinearSegmentedColormap.from_list(
    "blue_red", ["#184f95", "#6da7ec", "#f0efec", "#ef8e8d", "#b8302f"])


# ---- style ----------------------------------------------------------------

def apply() -> None:
    """Set matplotlib defaults: thin marks, quiet axes and grid, clear text."""
    mpl.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "figure.dpi": 110,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "text.color": INK,
        "axes.titlesize": 13,
        "axes.titleweight": "semibold",
        "axes.titlelocation": "left",
        "axes.titlepad": 12,
        "axes.labelcolor": INK_SECONDARY,
        "axes.labelsize": 10,
        "axes.edgecolor": AXIS,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "axes.axisbelow": True,
        "axes.prop_cycle": mpl.cycler(color=SLOTS),
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "grid.linestyle": "-",
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "xtick.labelcolor": INK_SECONDARY,
        "ytick.labelcolor": INK_SECONDARY,
        "xtick.major.size": 0,
        "ytick.major.size": 0,
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "legend.frameon": False,
        "legend.fontsize": 9,
        "patch.linewidth": 0,
    })


def rupees(value) -> str:
    """Label for one value: 182559 -> '₹1.83L', 38000 -> '₹38k'."""
    if abs(value) >= 1_00_000:
        lakhs = f"{value / 1_00_000:.2f}".rstrip("0").rstrip(".")
        return f"₹{lakhs}L"   # lakh, as Indian readers expect
    if abs(value) >= 1000:
        return f"₹{value / 1000:.0f}k"
    return f"₹{value:.0f}"


def _axis_rupees(value, _pos=None) -> str:
    """Axis ticks: ₹0, ₹500, ₹1.5k, ₹150k, −₹1k.

    Ticks never switch to lakh: mixing "₹75k" and "₹1L" on one axis makes
    readers stop and convert. Decimals are kept when needed, so two ticks
    never round to the same label (1.5k and 2k, not 2k and 2k).
    """
    if value == 0:
        return "₹0"
    sign = "−" if value < 0 else ""
    size = abs(value)
    if size < 1000:
        return f"{sign}₹{size:,.0f}"
    thousands = f"{size / 1000:,.1f}".rstrip("0").rstrip(".")
    return f"{sign}₹{thousands}k"


RUPEES = FuncFormatter(_axis_rupees)


def contrast_text(ax, values, threshold: float = 0.55) -> None:
    """Heatmap labels: white text on dark cells, black text on light cells."""
    flat = [v for row in values for v in row]
    low, high = min(flat), max(flat)
    for text, value in zip(ax.texts, flat):
        dark = (value - low) / (high - low) > threshold
        text.set_color("#ffffff" if dark else INK)


def only_grid(ax, axis: str = "y") -> None:
    """Keep the gridlines that help reading values; hide the others."""
    ax.grid(axis="x" if axis == "y" else "y", visible=False)


def title(ax, text: str, sub: str | None = None) -> None:
    """Title = the takeaway ("Revenue grew 2.7x"), subtitle = what is measured."""
    ax.set_title(text, pad=26 if sub else 12)
    if sub:
        ax.text(0, 1.03, sub, transform=ax.transAxes, color=INK_SECONDARY, fontsize=9.5, va="bottom")

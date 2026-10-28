"""Generate the practice dataset for topic 12 (an online shop, Jan-Jun 2026).

The data is deliberately messy, the way real data usually is:
  - the same city written in different ways ("Pune", " pune", "PUNE", "Bangalore" vs "Bengaluru")
  - missing quantities and payment methods
  - a few exact duplicate rows
  - a few impossible quantities (0 or negative)
  - a product ID that doesn't exist in products.csv

Run it again any time; the fixed seed always gives the same files:
    python 12_pandas/data/make_data.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
rng = np.random.default_rng(seed=2026)

products = pd.DataFrame({
    "product_id": [f"P{n:02d}" for n in range(1, 13)],
    "product": [
        "Wireless Earbuds", "Phone Charger", "Smart Watch",
        "Python Crash Course", "Data Science Handbook", "Notebook Pack",
        "Coffee Mug", "Desk Lamp", "Cushion Cover",
        "Cotton Kurta", "Running Shoes", "Denim Jacket",
    ],
    "category": ["Electronics"] * 3 + ["Books"] * 3 + ["Home"] * 3 + ["Clothing"] * 3,
    "price": [1999, 499, 4999, 899, 1299, 249, 349, 1199, 399, 1499, 2999, 2499],
})

n = 300
city_spellings = {
    "Pune": ["Pune", "pune", " Pune", "PUNE"],
    "Mumbai": ["Mumbai", "mumbai ", "Mumbai"],
    "Delhi": ["Delhi", "delhi", "New Delhi"],
    "Bengaluru": ["Bengaluru", "Bangalore", "bengaluru"],
    "Hyderabad": ["Hyderabad", "hyderabad"],
}
true_cities = rng.choice(list(city_spellings), size=n, p=[0.3, 0.25, 0.2, 0.15, 0.1])
cities = [rng.choice(city_spellings[c]) for c in true_cities]

days = pd.date_range("2026-01-01", "2026-06-30", freq="D")
# Later months get a bit more weight, so there is a growth trend to discover.
weights = np.linspace(1, 2, len(days))
order_dates = rng.choice(days, size=n, p=weights / weights.sum())

orders = pd.DataFrame({
    "order_id": range(1001, 1001 + n),
    "order_date": pd.to_datetime(order_dates).strftime("%Y-%m-%d"),
    "customer": rng.choice(
        ["Asha", "Ravi", "Meera", "Kabir", "Isha", "Arjun", "Neha", "Rohan",
         "Priya", "Vikram", "Sana", "Dev"], size=n),
    "city": cities,
    "product_id": rng.choice(products["product_id"], size=n,
                             p=[.12, .14, .05, .1, .06, .1, .1, .06, .07, .08, .06, .06]),
    "quantity": rng.choice([1, 1, 1, 2, 2, 3], size=n).astype(float),
    "payment_method": rng.choice(["UPI", "Card", "Cash on Delivery", "UPI"], size=n),
})

# ---- add the mess ---------------------------------------------------------
orders.loc[rng.choice(n, 12, replace=False), "quantity"] = np.nan
orders.loc[rng.choice(n, 8, replace=False), "payment_method"] = None
orders.loc[[17, 140], "quantity"] = [0, -2]
orders.loc[[55, 201, 260], "product_id"] = "P99"
duplicates = orders.loc[[3, 42, 99, 150, 222]]
orders = pd.concat([orders, duplicates]).sort_values("order_id").reset_index(drop=True)

products.to_csv(HERE / "products.csv", index=False)
orders.to_csv(HERE / "orders.csv", index=False)
print(f"Wrote {len(products)} products and {len(orders)} orders to {HERE}")

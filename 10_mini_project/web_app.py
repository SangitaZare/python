"""Expense Tracker: web version built with Streamlit.

Run it from the 10_mini_project folder (with the virtual environment active):

    streamlit run web_app.py

How Streamlit works, in one sentence: every time you click or type,
Streamlit runs this whole file again from top to bottom and redraws the
page. So we simply load the data at the top, draw everything, and save
after any change.

Notice what is NOT in this file: no business logic. Adding, deleting,
totals and saving all come from tracker.py, storage.py and models.py,
the exact same code the terminal app (main.py) uses.
"""
from datetime import date

import altair as alt
import pandas as pd
import streamlit as st

import storage
from errors import ExpenseError
from models import CATEGORIES
from reports import days_counted, month_name
from sample_data import demo_tracker
from tracker import ExpenseTracker

# The same colour for each category as in the terminal version.
CATEGORY_COLORS = {
    "bills": "#4C8DDB",
    "food": "#E3A92B",
    "shopping": "#A06BD8",
    "transport": "#24A897",
    "fun": "#E2607A",
    "health": "#4AA868",
    "other": "#8E99A6",
}


def money(amount: float) -> str:
    return f"₹{amount:,.0f}"


def to_dataframe(expenses) -> pd.DataFrame:
    """List of Expense objects -> pandas table (a first taste of Part 2)."""
    rows = [e.to_dict() for e in expenses]
    df = pd.DataFrame(rows, columns=storage.CSV_FIELDS)
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_tracker(path) -> ExpenseTracker:
    try:
        tracker = storage.load(path)
    except ExpenseError as e:
        st.error(f"{e}. Fix the file or move it away, then reload the page.")
        st.stop()
    if path == storage.DEMO_FILE and not len(tracker):
        tracker = demo_tracker()
        storage.save(tracker, path)
    return tracker


def save_and_rerun(tracker: ExpenseTracker, path, message: str) -> None:
    storage.save(tracker, path)
    # session_state survives the rerun, so the message can be shown after it.
    st.session_state["flash"] = message
    st.rerun()


# ---- page setup -----------------------------------------------------------

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

today = date.today()

# ---- sidebar: choose data, set budget, add an expense -----------------------

with st.sidebar:
    st.header("💰 Expense Tracker")
    source = st.radio(
        "Data",
        ["Demo data", "My expenses"],
        help="Demo data is saved to data/demo.json, your own to data/expenses.json",
    )
    path = storage.DEMO_FILE if source == "Demo data" else storage.DEFAULT_FILE
    tracker = load_tracker(path)

    new_budget = st.number_input(
        "Monthly budget (₹)", min_value=1000.0, step=1000.0, value=float(tracker.budget)
    )
    if new_budget != tracker.budget:
        tracker.budget = new_budget
        save_and_rerun(tracker, path, f"Budget set to {money(new_budget)}")

    st.subheader("Add expense")
    # A form groups the inputs, so the page only reruns when you press Add.
    with st.form("add_expense", clear_on_submit=True):
        amount = st.number_input("Amount (₹)", min_value=0.0, step=50.0, format="%.2f")
        category = st.selectbox("Category", CATEGORIES)
        description = st.text_input("Description", placeholder="e.g. Groceries")
        spent_on = st.date_input("Date", value=today, max_value=today, format="DD-MM-YYYY")
        submitted = st.form_submit_button("Add expense", type="primary", width="stretch")

    if submitted:
        try:
            expense = tracker.add(amount, category, description, spent_on)
        except ExpenseError as e:
            st.error(str(e))  # e.g. "Amount must be more than 0"
        else:
            save_and_rerun(tracker, path, f"Added #{expense.id}: {expense.description}, {money(expense.amount)}")

# ---- main area --------------------------------------------------------------

if flash := st.session_state.pop("flash", None):
    st.success(flash)

if not len(tracker):
    st.title("Expense Tracker")
    st.info("No expenses yet. Add your first one with the form on the left.")
    st.stop()

months = sorted({e.month for e in tracker}, reverse=True)
month = st.selectbox("Month", months, format_func=month_name)
rows = list(tracker.filter(month=month))
total = tracker.total(rows)
budget = tracker.budget

st.title(month_name(month))

# Key numbers in a row of metric cards.
col1, col2, col3, col4 = st.columns(4)
col1.metric("Spent", money(total), f"{len(rows)} expenses", delta_color="off")
if total <= budget:
    col2.metric("Budget left", money(budget - total), f"{total / budget:.0%} used", delta_color="off")
else:
    col2.metric("Over budget", money(total - budget), f"{total / budget:.0%} used", delta_color="inverse")
col3.metric("Daily average", money(total / days_counted(month, today)))
biggest = tracker.biggest(month)
col4.metric("Biggest expense", money(biggest.amount), biggest.description, delta_color="off")

st.progress(min(total / budget, 1.0), text=f"{total / budget:.0%} of your {money(budget)} budget")

summary_tab, table_tab, manage_tab = st.tabs(["📊 Summary", "📋 All expenses", "⚙️ Manage"])

# ---- tab 1: charts ----------------------------------------------------------

with summary_tab:
    totals = tracker.totals_by_category(month)
    by_category = pd.DataFrame({"category": list(totals), "amount": list(totals.values())})
    by_category["share"] = by_category["amount"] / total
    colors = alt.Scale(domain=list(CATEGORY_COLORS), range=list(CATEGORY_COLORS.values()))

    left, right = st.columns([3, 2])
    with left:
        st.subheader("Where the money went")
        bars = (
            alt.Chart(by_category)
            .mark_bar(cornerRadiusEnd=4)
            .encode(
                x=alt.X("amount:Q", title="Amount (₹)"),
                y=alt.Y("category:N", sort="-x", title=None),
                color=alt.Color("category:N", scale=colors, legend=None),
                tooltip=[
                    alt.Tooltip("category:N", title="Category"),
                    alt.Tooltip("amount:Q", title="Amount (₹)", format=",.0f"),
                    alt.Tooltip("share:Q", title="Share", format=".0%"),
                ],
            )
        )
        st.altair_chart(bars, width="stretch")
    with right:
        st.subheader("Share of spending")
        donut = (
            alt.Chart(by_category)
            .mark_arc(innerRadius=60)
            .encode(
                theta=alt.Theta("amount:Q"),
                color=alt.Color("category:N", scale=colors, legend=alt.Legend(title=None)),
                tooltip=[
                    alt.Tooltip("category:N", title="Category"),
                    alt.Tooltip("share:Q", title="Share", format=".0%"),
                ],
            )
        )
        st.altair_chart(donut, width="stretch")

    st.subheader("Spending by day")
    daily = to_dataframe(rows).groupby("date", as_index=False)["amount"].sum()
    st.bar_chart(daily, x="date", y="amount", x_label="Date", y_label="Amount (₹)")

# ---- tab 2: searchable table + download -------------------------------------

with table_tab:
    f1, f2 = st.columns([2, 3])
    chosen = f1.multiselect("Categories", CATEGORIES, placeholder="All categories")
    search = f2.text_input("Search description", placeholder="e.g. groceries")

    df = to_dataframe(tracker)
    if chosen:
        df = df[df["category"].isin(chosen)]
    if search:
        df = df[df["description"].str.contains(search, case=False, regex=False)]

    st.dataframe(
        df,
        hide_index=True,
        width="stretch",
        column_config={
            "id": st.column_config.NumberColumn("ID", width="small"),
            "date": st.column_config.DateColumn("Date", format="DD-MM-YYYY"),
            "category": "Category",
            "description": "Description",
            "amount": st.column_config.NumberColumn("Amount (₹)", format="₹%.2f"),
        },
    )
    st.caption(f"{len(df)} expenses · total {money(df['amount'].sum())}")
    st.download_button(
        "⬇️ Download as CSV",
        df.assign(date=df["date"].dt.strftime("%Y-%m-%d")).to_csv(index=False),
        file_name="expenses.csv",
        mime="text/csv",
    )

# ---- tab 3: delete ----------------------------------------------------------

with manage_tab:
    st.subheader("Delete an expense")
    options = {
        f"#{e.id} · {e.date:%d-%m-%Y} · {e.category} · {e.description} · {money(e.amount)}": e.id
        for e in tracker
    }
    picked = st.selectbox("Expense", list(options), index=None, placeholder="Choose an expense")
    confirm = st.checkbox("Yes, I want to delete it")
    if st.button("Delete", type="primary", disabled=not (picked and confirm)):
        removed = tracker.delete(options[picked])
        save_and_rerun(tracker, path, f"Deleted #{removed.id}: {removed.description}")

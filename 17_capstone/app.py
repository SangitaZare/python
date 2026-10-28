"""Campaign Planner: decide whom to call, and how many calls are worth making.

    streamlit run app.py        (from the 17_capstone folder, with the venv active)

The app replays the most recent 20% of the bank's calls as "the next campaign".
The model never saw these customers during training, so the numbers shown are
an honest backtest: what would have happened if the bank had followed the model.
"""
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

import bank_model as bm

BLUE, GREY, INK = "#2a78d6", "#898781", "#0b0b0b"

# What the user sees -> the code used in the dataset
PREVIOUS_CAMPAIGN = {"not contacted before": "nonexistent", "said no": "failure", "said yes": "success"}


@st.cache_resource
def get_model():
    return bm.load_or_train()


@st.cache_data
def get_campaign() -> pd.DataFrame:
    """The upcoming customers, each with the model's probability of saying yes."""
    _, upcoming = bm.split_by_time(bm.load_data())
    upcoming = upcoming.copy()
    upcoming["call_order"] = upcoming.index   # the original date order, kept before re-sorting
    upcoming["customer_id"] = [f"C-{n:05d}" for n in upcoming.index]
    upcoming["probability"] = get_model().predict_proba(upcoming[bm.FEATURES])[:, 1]
    return upcoming.sort_values("probability", ascending=False, kind="stable").reset_index(drop=True)


def euros(amount: float) -> str:
    return f"€{amount:,.0f}"


st.set_page_config(page_title="Campaign Planner", page_icon="📞", layout="wide")
campaign = get_campaign()
total = len(campaign)

# ---- sidebar: business assumptions ------------------------------------------

with st.sidebar:
    st.header("📞 Campaign Planner")
    st.caption("Change the assumptions to match your campaign.")
    cost = st.number_input("Cost per call (€)", min_value=1.0, max_value=100.0, value=8.0, step=1.0,
                           help="Agent time and phone costs for one call")
    value = st.number_input("Value of one sale (€)", min_value=1.0, max_value=1000.0, value=40.0, step=5.0,
                            help="Expected profit from one term-deposit subscription")

    gains = bm.gains_table(campaign["probability"], campaign["subscribed"], value, cost)
    best = gains.loc[gains["profit"].idxmax()]
    recommended = max(1, round(best["share_called"] * 100))
    st.success(f"Recommended: call the top **{recommended}%** of customers.")
    share = st.slider("Customers to call (%)", min_value=1, max_value=100, value=recommended,
                      help="Customers are called from most to least likely to say yes")

# ---- headline numbers ---------------------------------------------------------

calls = max(1, round(total * share / 100))
row = gains.iloc[calls - 1]
everyone = gains.iloc[-1]

st.title("Who should we call?")
st.caption(f"Backtest on the bank's {total:,} most recent customers, which the model never saw in training. "
           "Customers are ranked by the model's chance of a yes.")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Calls", f"{calls:,}", f"{share}% of the list", delta_color="off")
c2.metric("Sales", f"{int(row['sales']):,}", f"{row['sales'] - row['random_sales']:+,.0f} vs random order")
c3.metric("Success rate", f"{row['sales'] / calls:.0%}", f"{campaign['subscribed'].mean():.0%} if random", delta_color="off")
c4.metric("Profit", euros(row["profit"]), f"{row['profit'] - everyone['profit']:+,.0f} € vs calling everyone")

plan_tab, list_tab, score_tab = st.tabs(["📈 Plan", "📋 Call list", "🔎 Score a customer"])

# ---- tab 1: profit and gains charts -------------------------------------------

with plan_tab:
    curve = gains.iloc[np.linspace(0, total - 1, 200).astype(int)]
    long = pd.concat([
        pd.DataFrame({"called": curve["share_called"] * 100, "profit": curve["profit"], "order": "Model order"}),
        pd.DataFrame({"called": curve["share_called"] * 100, "profit": curve["random_profit"], "order": "Random order"}),
    ])
    colors = alt.Scale(domain=["Model order", "Random order"], range=[BLUE, GREY])
    lines = alt.Chart(long).mark_line(strokeWidth=2).encode(
        x=alt.X("called:Q", title="Customers called (%)", scale=alt.Scale(domain=[0, 100])),
        y=alt.Y("profit:Q", title="Profit (€)"),
        color=alt.Color("order:N", scale=colors, legend=alt.Legend(title=None, orient="bottom")),
        tooltip=[alt.Tooltip("order:N", title=" "), alt.Tooltip("called:Q", title="Called (%)", format=".0f"),
                 alt.Tooltip("profit:Q", title="Profit (€)", format=",.0f")],
    )
    choice = alt.Chart(pd.DataFrame({"called": [share]})).mark_rule(color=INK).encode(x="called:Q")
    left, right = st.columns([3, 2])
    with left:
        st.subheader("Profit by number of calls")
        st.altair_chart(lines + choice, width="stretch")
    with right:
        st.subheader("What this plan means")
        caught = row["sales"] / campaign["subscribed"].sum()
        st.markdown(
            f"- Calling the top **{share}%** ({calls:,} customers) catches **{caught:.0%}** of all possible sales.\n"
            f"- That's **{row['sales'] / max(row['random_sales'], 1):.1f}×** the sales of calling the same number at random.\n"
            f"- Compared with calling everyone: **{total - calls:,} fewer calls** and "
            f"**{euros(row['profit'] - everyone['profit'])}** difference in profit.\n"
            f"- The last customer called has a predicted chance of **{row['probability']:.0%}**."
        )
        st.info("The model is used to **order** calls, never to refuse a product to anyone.")

# ---- tab 2: the call list --------------------------------------------------------

with list_tab:
    st.subheader(f"Top {calls:,} customers to call")
    call_list = campaign.head(calls)[["customer_id", "probability", "age", "job", "marital", "contact", "poutcome"]].rename(
        columns={"customer_id": "Customer", "probability": "Chance of yes", "age": "Age", "job": "Job",
                 "marital": "Marital status", "contact": "Contact", "poutcome": "Previous campaign"})
    st.dataframe(
        call_list, hide_index=True, width="stretch",
        column_config={"Chance of yes": st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1)},
    )
    st.download_button("⬇️ Download call list (CSV)", call_list.to_csv(index=False), file_name="call_list.csv",
                       mime="text/csv")

# ---- tab 3: score one customer -----------------------------------------------------

with score_tab:
    st.subheader("How likely is this customer to say yes?")
    with st.form("score"):
        a, b, c = st.columns(3)
        age = a.number_input("Age", min_value=18, max_value=100, value=35)
        job = b.selectbox("Job", sorted(campaign["job"].unique()), index=0)
        marital = c.selectbox("Marital status", ["married", "single", "divorced", "unknown"])
        education = a.selectbox("Education", sorted(campaign["education"].unique()))
        housing = b.selectbox("Housing loan", ["no", "yes", "unknown"])
        loan = c.selectbox("Personal loan", ["no", "yes", "unknown"])
        contact = a.selectbox("Contact type", ["cellular", "telephone"])
        previous_answer = b.selectbox("Previous campaign", list(PREVIOUS_CAMPAIGN), key="poutcome")
        poutcome = PREVIOUS_CAMPAIGN[previous_answer]
        previous = c.number_input("Earlier contacts", min_value=1, max_value=10, value=1,
                                  help="Contacts in earlier campaigns (ignored if never contacted before)")
        submitted = st.form_submit_button("Score customer", type="primary")

    if submitted:
        # The most recent call (NOT the last row: the table is sorted by probability)
        # gives today's economic conditions and call timing.
        latest = campaign.loc[campaign["call_order"].idxmax()]
        customer = pd.DataFrame([{
            "age": age, "job": job, "marital": marital, "education": education, "default": "no",
            "housing": housing, "loan": loan, "contact": contact, "month": latest["month"],
            "day_of_week": latest["day_of_week"], "poutcome": poutcome,
            "previous": 0 if poutcome == "nonexistent" else previous,
            # Use the typical pdays for this answer: in the data, customers who said no last time
            # almost always have pdays = 999, while those who said yes were contacted ~5 days before.
            "pdays": campaign.loc[campaign["poutcome"] == poutcome, "pdays"].median(),
            **{col: latest[col] for col in ["emp.var.rate", "cons.price.idx", "cons.conf.idx", "euribor3m", "nr.employed"]},
        }])
        chance = get_model().predict_proba(bm.add_features(customer)[bm.FEATURES])[0, 1]
        rank = (campaign["probability"] > chance).mean()
        st.metric("Chance of saying yes", f"{chance:.0%}", f"average customer: {campaign['probability'].mean():.0%}",
                  delta_color="off")
        st.write(f"This customer would be in the **top {max(rank, 0.001):.0%}** of the call list.")

st.caption("Data: UCI Bank Marketing dataset (Moro et al., 2014), CC BY 4.0. Costs and values are assumptions; "
           "the use of age and job in targeting should be reviewed for fairness and compliance before real use.")

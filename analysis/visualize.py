#-------------Task 11 — Two visualizations (analysis/visualize.py)-------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- CHART 1: Return Rate by Payment Method ---
return_rates = (
    orders_merged.groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

# Colors: COD red, others grey
colors = [
    "#D60F0F" if method == "COD" else "#BDC3C7"
    for method in return_rates.index
]

# Create chart
fig, ax = plt.subplots(figsize=(7, 4))

bars = ax.bar(return_rates.index, return_rates.values, color=colors)

# Data labels
for bar, value in zip(bars, return_rates.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{value:.1f}%",
        ha="center",
        va="bottom"
    )

# Formatting
ax.set_title("COD Returns at 44.4% — 3x Card")
ax.set_xlabel("Payment Method")
ax.set_ylabel("Return Rate (%)")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# Save chart
os.makedirs("visualization", exist_ok=True)
plt.savefig(
    "visualization/return_rate_by_payment.png",
    dpi=150,
    facecolor="white"
)

plt.show()

# --- CHART 2: Outlier-Corrected Monthly Revenue Trend ---
import os
import matplotlib.pyplot as plt

# Outlier-corrected monthly revenue
monthly_revenue = (
    orders_merged[~orders_merged["is_outlier"]]
    .groupby("year_month")["order_value"]
    .sum()
)

# Chronological order
month_order = [
    "2026-01", "2026-02", "2026-03",
    "2026-04", "2026-05", "2026-06"
]
monthly_revenue = monthly_revenue.reindex(month_order)

# Create line chart
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(
    monthly_revenue.index,
    monthly_revenue.values,
    marker="o"
)

# Highlight March 2026
ax.scatter(
    "2026-03",
    monthly_revenue.loc["2026-03"],
    color="#E74C3C",
    s=120,
    zorder=5
)

# Annotate March
ax.annotate(
    "Mar: ₹20,318.90\n(actual peak)",
    xy=("2026-03", monthly_revenue.loc["2026-03"]),
    xytext=(15, 0),
    textcoords="offset points",
    fontsize=9,
    color="#E74C3C",
    ha="left",
    va="center"
)
# Chart formatting
ax.set_title("Outlier-Corrected Monthly Revenue — Peak: March 2026")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (₹)")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()

# Save chart
os.makedirs("visualizations", exist_ok=True)
plt.savefig(
    "visualizations/monthly_revenue_trend.png",
    dpi=150,
    facecolor="white"
)

plt.show()


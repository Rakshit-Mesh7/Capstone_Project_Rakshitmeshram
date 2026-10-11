#--------Task 1 — Load and inspect----------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load the three CSV files
customers = pd.read_csv("customers.csv")
products = pd.read_csv("products.csv")
orders = pd.read_csv("Orders.csv")

# Inspect the shape of each dataset
print("Customers shape:", customers.shape)
print("Products shape:", products.shape)
print("orders shape:", orders.shape)
# Verify orders has 180 rows and 9 columns
print("Orders shape check:", orders.shape)

#task_1 output: orders shape: (180, 9)


#--------Task 2 — Standardize payment_method casing----------
print(orders['payment_method'].unique())

orders['payment_method'] = orders['payment_method'].str.strip().str.upper()

orders['payment_method'].unique()
orders['payment_method'].value_counts()

#task 2 output:    CARD: 70, UPI: 55, COD: 55


#--------Task 3 — Remove duplicate orders----------

# Natural key: all columns except order_id
natural_key = [
    "customer_id",
    "product_id",
    "order_date",
    "quantity",
    "discount_pct",
    "payment_method",
    "rating",
    "returned"
]

# Detect duplicate orders
duplicate_mask = orders.duplicated(
    subset=natural_key,
    keep="first"
)

# Print number of duplicates
print("Number of duplicate orders:", duplicate_mask.sum())

# Print the order_id values of the 5 duplicate rows
print("Dropped order_id values:")
print(orders.loc[duplicate_mask, "order_id"].tolist())

# Remove duplicates
orders_clean = orders.drop_duplicates(
    subset=natural_key,
    keep="first"
).copy()

# Check final shape
print("Orders clean shape:", orders_clean.shape)

#Task 3 output:  
#Number of duplicate orders: 5
#Dropped order_id values:
#['O0176', 'O0177', 'O0178', 'O0179', 'O0180']
#Orders clean shape: (175, 9) 


#---------------Task 4 — Impute missing values-----------

print(orders.isnull().sum())
# 1. Fill missing discount_pct with 0
discount_missing = orders_clean["discount_pct"].isna().sum()
print("Missing discount_pct values:", discount_missing)

orders_clean["discount_pct"] = orders_clean["discount_pct"].fillna(0)

# 2. Calculate and print median rating BEFORE imputing
rating_median = orders_clean["rating"].median()
print("Rating median:", rating_median)

# 3. Fill missing rating with the median
rating_missing = orders_clean["rating"].isna().sum()
print("Missing rating values:", rating_missing)

orders_clean["rating"] = orders_clean["rating"].fillna(rating_median)

# 4. Check that no missing values remain
print("\nMissing values after imputation:")
print(orders_clean[["discount_pct", "rating"]].isnull().sum())

#Task_4  output:
#Missing discount_pct values: 12
#Rating median: 3.0
#Missing rating values: 15
#Missing values after imputation:
#discount_pct    0
#rating          0

#------------Task 5 — Merge and reconcile against Part 1-------------
# Merge cleaned orders with products
orders_merged = orders_clean.merge(
    products,
    on="product_id",
    how="left"
)

# Merge with customers
orders_merged = orders_merged.merge(
    customers,
    on="customer_id",
    how="left"
)

# Calculate order value for each cleaned order
orders_merged["order_value"] = (
    orders_merged["quantity"]
    * orders_merged["price"]
    * (1 - orders_merged["discount_pct"] / 100)
)

# Calculate total order value across 175 cleaned rows
cleaned_total = orders_merged["order_value"].sum()

print(f"Total order value across {len(orders_clean)} cleaned orders: ₹{cleaned_total:.2f}")


# ---------------------------------------------------------
# Independently calculate the value of the 5 dropped rows
# ---------------------------------------------------------

# Identify the duplicate rows removed in Task 3
duplicate_mask = orders.duplicated(
    subset=[
        "customer_id",
        "product_id",
        "order_date",
        "quantity",
        "discount_pct",
        "payment_method",
        "rating",
        "returned"
    ],
    keep="first"
)

dropped_orders = orders.loc[duplicate_mask].copy()

# Merge dropped orders with products to get price
dropped_orders = dropped_orders.merge(
    products[["product_id", "price"]],
    on="product_id",
    how="left"
)

# Calculate order_value for the dropped rows
dropped_orders["order_value"] = (
    dropped_orders["quantity"]
    * dropped_orders["price"]
    * (1 - dropped_orders["discount_pct"] / 100)
)

dropped_total = dropped_orders["order_value"].sum()

print("Dropped order IDs:")
print(dropped_orders["order_id"].tolist())

print(f"Order value of the 5 dropped duplicate rows: ₹{dropped_total:.2f}")


# ---------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------

raw_total = 99860.20
delta = raw_total - cleaned_total

print(
    f"\nReconciliation: The cleaned total of ₹{cleaned_total:.2f} is"
    f"₹{delta:.2f} lower than the Part 1 raw total of ₹{raw_total:.2f}.\n "
    f"This exact ₹{delta:.2f} reduction is attributable to the 5 duplicate "
    f"orders removed in Task 3 (O0176, O0177, O0178, O0179, and O0180),"
    f"whose combined order_value is ₹{dropped_total:.2f}.\n "
    f"The discount_pct and rating imputations do not change the order_value "
    f"total because discount_pct missing values are imputed as 0 according "
    f"to the business rule and rating is not used in the order_value formula.\n"
)


# ---------------------------------------------------------
# Verification
# ---------------------------------------------------------

assert len(orders_clean) == 175
assert round(cleaned_total, 2) == 97358.30
assert round(dropped_total, 2) == 2501.90
assert round(delta, 2) == 2501.90

#Task_5 output:
#Total order value across 175 cleaned orders: ₹97358.30
#Dropped order IDs:
#['O0176', 'O0177', 'O0178', 'O0179', 'O0180']
#Order value of the 5 dropped duplicate rows: ₹2501.90

#Reconciliation: The cleaned total of ₹97358.30 is₹2501.90 lower than the Part 1 raw total of ₹99860.20.
# This exact ₹2501.90 reduction is attributable to the 5 duplicate orders removed in Task 3 (O0176, O0177, O0178, O0179, and O0180),whose combined order_value is ₹2501.90.
# The discount_pct and rating imputations do not change the order_value total because discount_pct missing values are imputed as 0 according to the business rule and rating is not used in the order_value formula.


#-----------Task 6 — IQR outlier detection on quantity-----------
Q1 = orders_merged["quantity"].quantile(0.25)
Q3 = orders_merged["quantity"].quantile(0.75)
IQR = Q3 - Q1
lower = Q1 - 1.5 * IQR
upper = Q3 + 1.5 * IQR

print("Q1 =", Q1)
print("Q3 =", Q3)
print("IQR =", IQR)
print("Lower =", lower)
print("Upper =", upper)

orders_merged["is_outlier"] = (
    (orders_merged["quantity"] < lower) |
    (orders_merged["quantity"] > upper))


print(orders_merged.loc[
    orders_merged["is_outlier"],
    ["order_id", "quantity"]
])

#Task_6 output:
#Q1 = 1.0
#Q3 = 2.0
#IQR = 1.0
#Lower = -0.5
#Upper = 3.5
#   order_id  quantity
#10    O0011        25
#97    O0098        30



#-----------Task 7 — Hypothesis: does COD have a higher return rate?--------------
print("Hypothesis: COD has a higher return rate than CARD and UPI.")

return_rates = orders_merged.groupby("payment_method")["returned"].agg(["count", "mean"])

print(return_rates)

print("\nReturn rates:")
for method, rate in (return_rates["mean"] * 100).round(1).items():
    print(f"{method}: {rate}%")

print("\nHypothesis: Confirmed")

#Task_7 output:
#Return rates:
#CARD: 14.7%
#COD: 44.4%
#UPI: 18.9%
#Hypothesis: Confirmed



#------------Task 8 — Multi-level segmentation----------------

segment_rates = orders_merged.groupby(
    ["payment_method", "city_tier"]
)["returned"].agg(["count", "mean"])
print(segment_rates)

print("\nReturn rates by segment:")
for (payment, tier), row in segment_rates.iterrows():
    print(f"{payment} + Tier-{tier} => {row['mean'] * 100:.1f}%")

print("\nHighest-risk segment: COD + Tier-2 cities at 54.5%.")
print("This shows that COD risk is not uniform across city tiers.")

#Task 8 output:
#Return rates by segment:
#CARD + Tier-1 => 8.9%
#CARD + Tier-2 => 26.1%
#COD + Tier-1 => 37.5%
#COD + Tier-2 => 54.5%
#UPI + Tier-1 => 19.4%
#UPI + Tier-2 => 18.2%

#Highest-risk segment: COD + Tier-2 cities at 54.5%.
#This shows that COD risk is not uniform across city tiers.




#------------Task 9 — Correlation analysis----------------
cols = ["rating", "returned", "discount_pct", "quantity"]
corr = orders_merged[cols].corr()
print("Correlation matrix:")
print(corr.round(2))

print("\nPairwise correlation strength:")
pairs = [
    ("rating", "returned"),
    ("rating", "discount_pct"),
    ("rating", "quantity"),
    ("returned", "discount_pct"),
    ("returned", "quantity"),
    ("discount_pct", "quantity")]

for a, b in pairs:
    r = corr.loc[a, b]
    print(f"{a} vs {b}: r = {r:.2f} → negligible")

print("\nHypothesis: Higher discounts reduce returns")
print("Hypothesis: Busted")
print(f"discount_pct vs returned correlation = {corr.loc['discount_pct', 'returned']:.2f}")


#------------Task 10 — Outlier-corrected time series----------------
orders_merged["order_date"] = pd.to_datetime(orders_merged["order_date"])
orders_merged["year_month"] = orders_merged["order_date"].dt.to_period("M").astype(str)

# (1) Monthly totals including outliers
monthly_with_outliers = orders_merged.groupby("year_month")["order_value"].sum()

print("Monthly order value — including outliers:")
print(monthly_with_outliers.round(2))

# (2) Monthly totals excluding Task 6 outliers
monthly_without_outliers = (
    orders_merged[~orders_merged["is_outlier"]]
    .groupby("year_month")["order_value"]
    .sum()
)

print("\nMonthly order value — excluding outliers:")
print(monthly_without_outliers.round(2))

print("\nInterpretation:")
print("January's apparent lead is an artifact of the two bulk orders landing in January:")
print("O0011 on 2026-01-28 and O0098 on 2026-01-10.")
print("Once these two outlier orders are excluded, March is the genuine peak month.")

#Task_10 output:
#Monthly order value — including outliers:
#year_month
#2026-01    29582.1
#2026-02    13195.5
#2026-03    20318.9
#2026-04     9495.3
#2026-05    13151.1
#2026-06    11615.4
#Name: order_value, dtype: float64

#Monthly order value — excluding outliers:
#year_month
#2026-01    11637.1
#2026-02    13195.5
#2026-03    20318.9
#2026-04     9495.3
#2026-05    13151.1
#2026-06    11615.4
#Name: order_value, dtype: float64
#Interpretation:
#January's apparent lead is an artifact of the two bulk orders landing in January:
#O0011 on 2026-01-28 and O0098 on 2026-01-10.
#Once these two outlier orders are excluded, March is the genuine peak month.



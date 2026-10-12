# Mamaearth Sales & Returns Analytics

## Overview

This project analyzes Mamaearth customer, product, and order data to understand revenue performance, investigate product returns, identify higher-risk order segments, and turn the verified results into a business-focused narrative.

The project is organized into three parts:

1. **Part 1 — SQL Relational Layer & Reporting:** create the relational schema, load the supplied records, and run SQL reports.
2. **Part 2 — Python/Pandas Data Wrangling & EDA:** clean the data, handle missing values and duplicates, calculate revenue, investigate returns and outliers, and create visualizations.
3. **Part 3 — GenAI-Powered Insight Narrator:** read the verified findings from JSON and generate a narrative using Gemini when a key is available, or the project's offline fallback when no key is set.

The key findings recorded for this dataset include 175 orders after five duplicate rows are removed, cleaned revenue of ₹97,358.30, a COD return rate of 44.4%, a 54.5% return rate for the COD + Tier-2 segment, and corrected peak monthly revenue of ₹20,318.90 in March 2026.

## Repository Structure

```text
.
├── analysis/
│   ├── clean_and_eda.py
│   └── visualize.py
├── data/
│   ├── Orders.csv
│   ├── customers.csv
│   └── products.csv
├── narrator/
│   ├── Sample_output.txt
│   ├── findings.json
│   └── generate_narrative.py
├── sql/
│   ├── reports.sql
│   ├── schema.sql
│   └── seed_data.sql
├── visualizations/
│   ├── monthly_revenue_trend.png
│   └── return_rate_by_payment.png
└── README.md
```

## Prerequisites

- Python 3.10 or later
- SQLite command-line tool (`sqlite3`)
- Python packages: `pandas`, `matplotlib`, and `google-genai` for Gemini-based narrative generation

Install the Python dependencies from the repository root:

```bash
pip install pandas matplotlib google-genai
```

Run every command below from the repository root unless noted otherwise.

---

## Part 1 — SQL Relational Layer & Reporting

### 1. Create the database schema

```bash
sqlite3 mamaearth.db < sql/schema.sql
```

This creates the `customers`, `products`, and `orders` tables.

### 2. Load the seed data

```bash
sqlite3 mamaearth.db < sql/seed_data.sql
```

This loads the records into the database. Run the schema script before the seed script.

### 3. Run the SQL reports

```bash
sqlite3 -header -column mamaearth.db < sql/reports.sql
```

The report output is displayed in the terminal.

### 4. Verify the original record counts

```bash
sqlite3 mamaearth.db "
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders;
"
```

Expected counts before Python cleaning:

| Table | Expected rows |
|---|---:|
| `customers` | 45 |
| `products` | 16 |
| `orders` | 180 |

If `sqlite3` is not recognized as a command, install SQLite and ensure its command-line executable is available on your PATH.

---

## Part 2 — Python/Pandas Data Wrangling & EDA

### 1. Clean the data and run EDA

```bash
python analysis/clean_and_eda.py
```

The script uses the CSV files under `data/`. It cleans the order data, removes duplicate orders, handles missing values, merges orders with customer and product information, calculates order revenue, flags quantity outliers, and analyzes returns and monthly revenue.

**Task 5 of Part 2 writes the verified findings to `narrator/findings.json`.** This file is the handoff from the analysis stage to the narrative generator. Run the cleaning/EDA script successfully before running Part 3.

The expected cleaned dataset contains 175 orders after five duplicate records are removed. Missing `discount_pct` values are filled with `0`, and missing ratings are filled using the median rating.

### 2. Create the visualizations

After the cleaning/EDA step completes, run:

```bash
python analysis/visualize.py
```

The expected visualization files are:

- `visualizations/return_rate_by_payment.png`
- `visualizations/monthly_revenue_trend.png`

The first chart compares return rates by payment method. The second shows monthly revenue after excluding the flagged quantity outliers from the trend calculation.

---

## Part 3 — GenAI-Powered Insight Narrator

The narrative generator reads the verified metrics from `narrator/findings.json`. Run it after completing Part 2.

### Option A — Run with a Gemini API key

Set the API key as an environment variable, then execute the script.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your-gemini-api-key"
python narrator/generate_narrative.py
```

**macOS / Linux (Bash):**

```bash
export GEMINI_API_KEY="your-gemini-api-key"
python narrator/generate_narrative.py
```

Replace `your-gemini-api-key` with your own key. Keep the key private: do not hard-code it in the script, add it to `findings.json`, or commit it to GitHub.

### Option B — Run without a Gemini API key (offline path)

The project is intended to support an offline fallback that generates the narrative from the existing verified findings without making a Gemini API request.

**Windows PowerShell:**

```powershell
Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
python narrator/generate_narrative.py
```

**macOS / Linux (Bash):**

```bash
unset GEMINI_API_KEY
python narrator/generate_narrative.py
```

For this path to work, `narrator/generate_narrative.py` must check whether `GEMINI_API_KEY` is missing and explicitly run the offline fallback. If the script currently only reads a key from Google Colab userdata, update it to support the environment variable and no-key fallback described above.

---

## Verified Findings

Use the values in `narrator/findings.json` as the source of truth for the narrative. The expected results for this dataset are:

| Metric | Expected result |
|---|---:|
| Original order records | 180 |
| Cleaned order records | 175 |
| Raw revenue before duplicate removal | ₹99,860.20 |
| Cleaned revenue | ₹97,358.30 |
| Revenue difference from duplicate removal | ₹2,501.90 |
| COD return rate | 44.4% |
| CARD return rate | 14.7% |
| UPI return rate | 18.9% |
| Highest-risk segment | COD + Tier-2 |
| COD + Tier-2 return rate | 54.5% |
| True peak month after outlier correction | March 2026 |
| Corrected March revenue | ₹20,318.90 |
| Apparent January revenue before outlier correction | ₹29,582.10 |
| Corrected January revenue | ₹11,637.10 |

Five duplicate order rows account for the ₹2,501.90 difference between raw and cleaned revenue. Two unusually large quantity orders, `O0011` and `O0098`, inflate January's apparent revenue. After those flagged rows are excluded from the monthly comparison, March 2026 is the true revenue peak.

To inspect the findings file:

**Windows Command Prompt:**

```cmd
type narrator\findings.json
```

**macOS / Linux:**

```bash
cat narrator/findings.json
```

---

## Final Reproduction Checklist

- [ ] Run `sql/schema.sql`.
- [ ] Run `sql/seed_data.sql`.
- [ ] Run `sql/reports.sql`.
- [ ] Verify the source counts: 45 customers, 16 products, and 180 orders.
- [ ] Run `analysis/clean_and_eda.py`.
- [ ] Confirm Task 5 writes `narrator/findings.json`.
- [ ] Run `analysis/visualize.py`.
- [ ] Confirm both PNG files exist in `visualizations/`.
- [ ] Run `narrator/generate_narrative.py` with `GEMINI_API_KEY` set.
- [ ] Run the narrative generator with the key unset and verify the offline fallback.
- [ ] Confirm the generated narrative uses the verified figures in `narrator/findings.json`.

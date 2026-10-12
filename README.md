# Mamaearth Sales & Returns Analytics

## Repository Structure

```text
.
├── README.md
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
└── visualizations/
    ├── monthly_revenue_trend.png
    └── return_rate_by_payment.png
```

## 1. Run the SQL pipeline

Run all commands from the repository root.

### Create the database schema

```bash
sqlite3 mamaearth.db < sql/schema.sql
```

### Load the seed data

```bash
sqlite3 mamaearth.db < sql/seed_data.sql
```

### Run the SQL reports

```bash
sqlite3 -header -column mamaearth.db < sql/reports.sql
```

### Verify the source record counts

```bash
sqlite3 mamaearth.db "
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'orders', COUNT(*) FROM orders;
"
```

Expected counts: 45 customers, 16 products, and 180 original orders.

## 2. Run the Python analysis and visualizations

### Clean the data and perform EDA

```bash
python analysis/clean_and_eda.py
```

The script reads the CSV files from `data/`. It cleans the order data, removes duplicate orders, handles missing values, merges the order, customer, and product data, calculates revenue, flags quantity outliers, and analyzes returns and monthly revenue.

**Task 5 of Part 2 writes the verified findings to `narrator/findings.json`.** Run this script successfully before generating the narrative.

### Generate the visualizations

```bash
python analysis/visualize.py
```

The expected outputs are:

- `visualizations/return_rate_by_payment.png`
- `visualizations/monthly_revenue_trend.png`

## 3. Generate the narrative

The narrative generator uses `narrator/findings.json` as its input.

### Option A — Run with a Gemini API key

Install the dependencies if needed:

```bash
pip install pandas matplotlib google-genai
```

Set the API key as an environment variable.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your-gemini-api-key"
python narrator/generate_narrative.py
```

**macOS / Linux:**

```bash
export GEMINI_API_KEY="your-gemini-api-key"
python narrator/generate_narrative.py
```

The script should read the key from `GEMINI_API_KEY` and use Gemini to generate the narrative. Do not hard-code your API key or commit it to the repository.

### Option B — Run without a Gemini API key

The project should also support an offline fallback that generates a narrative from the verified findings without calling Gemini.

**Windows PowerShell:**

```powershell
Remove-Item Env:GEMINI_API_KEY -ErrorAction SilentlyContinue
python narrator/generate_narrative.py
```

**macOS / Linux:**

```bash
unset GEMINI_API_KEY
python narrator/generate_narrative.py
```

When no key is available, the script should use the offline fallback. This path should not require a Gemini API request.

## 4. Verify the findings

Inspect the generated findings file:

**Windows Command Prompt:**

```cmd
type narrator\findings.json
```

**macOS / Linux:**

```bash
cat narrator/findings.json
```

The results should include the following verified figures:

| Finding                                            | Expected value |
| -------------------------------------------------- | -------------: |
| Original orders                                    |            180 |
| Cleaned orders                                     |            175 |
| Raw revenue                                        |     ₹99,860.20 |
| Cleaned revenue                                    |     ₹97,358.30 |
| Revenue difference from duplicate removal          |      ₹2,501.90 |
| COD return rate                                    |          44.4% |
| CARD return rate                                   |          14.7% |
| UPI return rate                                    |          18.9% |
| Highest-risk segment                               |   COD + Tier-2 |
| COD + Tier-2 return rate                           |          54.5% |
| Corrected revenue peak                             |     March 2026 |
| Corrected March revenue                            |     ₹20,318.90 |
| Apparent January revenue before outlier correction |     ₹29,582.10 |
| Corrected January revenue                          |     ₹11,637.10 |

Five duplicate order rows are removed during cleaning. The January revenue peak is inflated by two unusually large quantity orders, `O0011` and `O0098`. After excluding the flagged outlier orders from the monthly comparison, March 2026 is the true revenue peak.

## 5. Final reproduction checklist
Final output:
Numeric accuracy checklist:
PASS — Cleaned total revenue (97,358.30)
PASS — COD return rate (44.4%)
PASS — COD + Tier-2 return rate (54.5%)
PASS — Duplicate reconciliation delta (2,501.90)
PASS — March peak revenue (20,318.90)

Overall result: PASS

Task 5 numeric accuracy checklist passed!

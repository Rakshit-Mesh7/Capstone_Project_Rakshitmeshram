## Overview

This project analyzes Mamaearth's customer, product, and order data to evaluate revenue performance, identify return patterns, and generate actionable business insights. The project is divided into three parts:

### Part 1 — SQL Relational Layer & Reporting

A relational database is created using SQL with three tables: `customers`, `products`, and `orders`. The source data is loaded using seed scripts, and SQL reports are executed to analyze order data and establish the foundation for further analysis.

### Part 2 — Python/Pandas Data Wrangling & EDA

Python and pandas are used to clean and prepare the data for analysis. This includes removing duplicate orders, handling missing values, merging customer and product information with orders, calculating revenue, identifying quantity outliers, and exploring return rates by payment method and city tier. Matplotlib is used to visualize return patterns and monthly revenue trends. Verified findings are saved to `narrator/findings.json` for the next stage.

### Part 3 — GenAI-Powered Insight Narrator

The narrative generator, `narrator/generate_narrative.py`, uses the verified findings in `narrator/findings.json` to produce a business-focused narrative for decision-makers. It supports Gemini API-based generation when an API key is available and an offline fallback when no key is provided.

### Key Findings

- **Data quality:** Five duplicate order rows are removed, leaving 175 cleaned orders.
- **Revenue reconciliation:** Cleaned revenue is ₹97,358.30, compared with raw revenue of ₹99,860.20.
- **Payment-method risk:** COD has the highest return rate at 44.4%, compared with 14.7% for CARD and 18.9% for UPI.
- **High-risk segment:** COD orders in Tier-2 cities have a return rate of 54.5%.
- **Revenue trend:** After correcting for unusually large quantity orders, March 2026 is the peak revenue month at ₹20,318.90.

The overall objective is to transform raw transactional data into reliable reports, clear visualizations, and actionable business recommendations.

---
name: data-summary
description: >
  Churn data-health audit and findings memo for this repo.
  Use for a data summary, data audit, findings memo, or EDA writeup
  on ecommerce_churn / churn data.
---

# Data summary

One job: audit the churn extract, write the chart and memo, then pass the check.

Two rules that matter on this dataset:

1. Collapse payment aliases before any group-by. Never leave `CC` and `Credit Card` as separate rows.
2. Do not silently fill `Tenure`. Report the gaps. Plot what is actually there.

## Files

- Data: `./data/ecommerce_churn.csv`
- Chart: `./outputs/churn_tenure.png`
- Memo: `./outputs/data_summary_memo.md`
- Breakdown column: `PreferredPaymentMode`

## Payment aliases

Map these before grouping:

| Raw | Use |
| :--- | :--- |
| `CC` | `Credit Card` |
| `COD` | `Cash on Delivery` |
| `E wallet` / `Ewallet` | `E-Wallet` |

Leave `Credit Card`, `Cash on Delivery`, `E-Wallet`, `UPI`, and `Debit Card` as they are.

## Tenure and other missing values

Report missing counts and ratios before you decide what to do.

For `Tenure`: no quiet median-impute to make a prettier chart. If you drop rows, say how many. If you impute later, say so in the memo.

Other columns with holes: note them. Do not impute unless asked.



## Memo

Write the memo as Markdown, these sections, in this order. Use numbers from this run.

**1. Overview**  
Size, e-commerce churn, what you audited. List the files this run produced.

**2. Health**  
Row and column count. Duplicate `CustomerID`s. Overall churn rate. Payment labels raw vs after cleanup.

Table for columns with issues, plus Tenure and payment mode:

| Column | Type | Missing count | Missing % | Status |
| :--- | :--- | ---: | ---: | :--- |

Status is one of: `IS_CLEAN` (no missing), `HAS_NULLS` (some missing), `SHOULD_REVIEW` (Tenure or messy labels that change how you read the result).

Missing %: `(null_count / total_rows) * 100`, two decimals.

**3. Breakdown**  
Churn by payment mode after aliases. Counts, share of rows, mean churn rate.

**4. Chart**  
Embed `![Churn by Tenure](./churn_tenure.png)`. One sentence on what it shows, plus the Tenure gap.

**5. Takeaways**  
Three bullets: one finding, one data-quality risk, one next step. Do not invent recommendations the tables and chart do not support.



## Done

```
.\.venv\Scripts\python.exe checks/review_outputs.py
```

Fix and re-run until it prints `passed`.

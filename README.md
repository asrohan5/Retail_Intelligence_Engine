This is one of the personal projects that i have taken up.
More on this soon.

## Data Integrity Audit (Day 2 Findings)
*Executed on 10% Sample (~54k rows)*

### 1. Data Quality Flags
* **Ghost Customers:** ~25% of transactions (13,547 rows) are anonymous (Guest Checkout).
    * *Impact:* Cannot calculate LTV or Retention for this segment.
    * *Action:* Excluded from RFM analysis; analyzed separately for "Walk-in" trends.
* **Inventory Adjustments:** Found 241 rows with `Price=0`.
    * *Observation:* Net quantity is **-13,290**. These represent stock write-offs/damages, not customer sales.
    * *Action:* Strictly filtered out for Revenue Reporting.
* **StockCode Pollution:** 177 StockCodes share multiple Descriptions (e.g., *'Paper Craft Little Birdie'* vs *'Paper Craft , Little Birdie'*).
    * *Action:* Standardized to the most recent description.

### 2. Business Logic Insights
* **Value Gap:** Registered users spend **84% more per transaction** (£22.76) compared to Guest users (£12.35).
* **Whale Transactions:** The Quantity distribution is highly skewed. Any order > 24 units is statistically an outlier.
* **Temporal Gaps:** Identified an 11-day gap in data. Requires verification against holiday calendar (likely Christmas shutdown).
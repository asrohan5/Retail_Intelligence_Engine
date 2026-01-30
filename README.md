This is one of the personal projects that i have taken up.
More on this soon.

## PART 2: Data Integrity Audit 
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


## 📊 PART 3: The Metrics Engine
*Focus: Transforming cleaned data into actionable Business Intelligence.*

Developed the `metrics.py` module, which serves as the core logic layer of the pipeline. Unlike basic analysis, this module uses professional retail frameworks (RFM & Cohort Analysis) to evaluate customer health.

### 1. Technical Implementation
* **RFM Segmentation:** Developed a quintile-based scoring system to categorize customers based on **Recency** (last purchase), **Frequency** (count of orders), and **Monetary** (total spend).
* **Cohort Analysis:** Built a dynamic cohort indexing function that tracks user retention over a 12-month lifecycle.
* **Executive KPI Table:** Engineered a summary logic that calculates Monthly Revenue, Month-over-Month (MoM) Growth, Active User counts, and Average Order Value (AOV).

### 2. Strategic Insights 
* **The Loyalty Core:** Identified **277 "Champions"**—customers with perfect RFM scores who represent the highest lifetime value.
* **Retention Trends:** Observed a strong Month-1 retention (~31%) for the Dec 2010 cohort, but identified a significant "churn gap" in the March 2011 cohort that requires further investigation.
* **AOV Analysis:** The Average Order Value hovers around **£75**, with a noticeable dip in December 2011 (likely due to incomplete data/early month cutoff).

### 3. Key Functions in `src/metrics.py`
* `calculate_rfm()`: Automates the shopper segmentation process.
* `calculate_cohort_index()`: Normalizes transaction dates to track user behavior over time.
* `build_executive_summary()`: Generates the final data frame used for C-suite reporting.
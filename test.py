import pandas as pd
import numpy as np
from src import config
from src import ingestion
import os

#os.makedirs('info', exist_ok = True)

# df_full = pd.read_excel(config.RAW_DATA_PATH, sheet_name = config.SHEET_NAME)
# df = df_full.sample(frac=config.SAMPLE_FRAC, random_state = config.RANDOM_STATE)


# df_columns = df.columns
# df_columns.to_series().to_csv('info/df_columns.txt', index=False, header=False)
# print('Columns exported')


from src.ingestion import load_and_optimize_data
from src.metrics import *

# 1. Load
df_raw = load_and_optimize_data()

# 2. Clean (Exercise 1)
df = clean_data_for_metrics(df_raw)

# 3. RFM Analysis (Exercise 2-4)
rfm = calculate_rfm_values(df)
rfm = assign_rfm_scores(rfm)
rfm = define_customer_segments(rfm)
print("--- Segment Distribution ---")
print(rfm['Segment'].value_counts())

# 4. Cohort Analysis (Exercise 5-6)
df = calculate_cohort_index(df)
retention = get_retention_matrix(df)
print("\n--- Retention Head (First 3 Months) ---")
print(retention.iloc[:, 0:4].head()) 

# 5. Executive Summary (Exercise 10)
exec_summary = build_executive_summary(df)
print("\n--- Executive Summary ---")
print(exec_summary.tail())
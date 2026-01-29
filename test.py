import pandas as pd
import numpy as np
from src import config
from src import ingestion
import os

#os.makedirs('info', exist_ok = True)

df_full = pd.read_excel(config.RAW_DATA_PATH, sheet_name = config.SHEET_NAME)
df = df_full.sample(frac=config.SAMPLE_FRAC, random_state = config.RANDOM_STATE)


# df_columns = df.columns
# df_columns.to_series().to_csv('info/df_columns.txt', index=False, header=False)
# print('Columns exported')

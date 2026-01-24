#src/ingestion.py

import pandas as pd
import numpy as np
import os
import sys
import logging
from src import config

os.makedirs('logs', exist_ok = True)
logging.basicConfig(
    level=logging.INFO,
    format = "%(asctime)s [%(levelname)s] %(message)s", handlers=[logging.FileHandler(config.LOG_FILE), logging.StreamHandler(sys.stdout)]
)

def load_and_optimize_data():
    try:
        logging.info(f'\n*******\nLoading Data from {config.RAW_DATA_PATH}....')

        df_full = pd.read_excel(config.RAW_DATA_PATH, sheet_name = config.SHEET_NAME)

        initial_mem = df_full.memory_usage(deep=True).sum()/(1024**2)
        logging.info(f'Initial memory usage: {initial_mem:.2f} MB ...')

        logging.info(f'Sampling {config.SAMPLE_FRAC*100}% of data')
        df = df_full.sample(frac=config.SAMPLE_FRAC, random_state = config.RANDOM_STATE)
        

        df['Country'] = df['Country'].astype('category')

        final_mem = df.memory_usage(deep=True).sum() / (1024**2)
        logging.info(f'Optimized Memory Usage: {final_mem:.2f} MB')
        logging.info(f'Reduction in memory: {((initial_mem/10 - final_mem)/(initial_mem/100))*100:.2f}%...')

        return df.reset_index(drop=True)

    except FileNotFoundError:
        logging.error('File nor found! Please check the data directory')
        return None

    except Exception as e:
        logging.error(f'An unexpected error occured: {e}')
        return None

if __name__ == '__main__':
    data = load_and_optimize_data()
    if data is not None:
        print(data.head())
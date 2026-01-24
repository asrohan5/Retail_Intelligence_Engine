import os

RAW_DATA_PATH = "data/online_retail_II.xlsx"
SHEET_NAME = 'Year 2010-2011'
LOG_FILE = 'logs/pipeline.log'

#Sampling Parameter
SAMPLE_FRAC = 0.1
RANDOM_STATE = 42

#Expected Schema

SCHEMA = {
    'Invoice':str,
    'StockCode':str,
    'Description':str,
    'Quantity': int,
    'Price': float,
    'Customer ID': float,
    'Country': 'category'

}

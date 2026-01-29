#Identification of Data Leaks and Logic Breaches
#src\validation

import numpy as np
import pandas as pd
import os
import sys
from src import config
import logging


logger = logging.getLogger(__name__)


#Auditing unique entitites to spot duplication or sparsity
def check_uniques(df):
    stats = {
        "unique_invoices": df['Invoice'].nunique(),
        "unique_stock_codes": df['StockCode'].nunique(),
        "unique_customer": df['Customer ID'].nunique()
    }
    logger.info(f'Unique Entity Audit: {stats}')
    return stats

#To identify potential freebies or data errors
def check_zero_prices(df):
    zero_prices_df = df[df['Price']<=0]
    percentage_zero = (len(zero_prices_df)/len(df))*100
    affected_quantity = zero_prices_df['Quantity'].sum()

    logger.info(f'Zero-Price rows: {len(zero_prices_df)} ({percentage_zero:.2f}%)')
    logger.info(f'Volume moved for free: {affected_quantity}')

    return zero_prices_df


#To fin StockCodes with multiple different description
def check_description_consistency(df):
    description_counts = df.groupby('StockCode')['Description'].nunique()
    inconsistency = description_counts[description_counts>1]

    if not inconsistency.empty:
        top_examples = inconsistency.sort_values(ascending=False).head(3)
        logger.warning(f'Red Flag: {len(inconsistency)} StockCodes have multiple description')
        logger.warning(f'Top offenders: \n {top_examples}')
    else:
        logger.info('Data Cleanliness: All Stockcodes have consistent descriptions')

    return inconsistency


#Check for missing Data Periods
def check_temporal_gaps(df):
    df_sorted = df.sort_values('InvoiceDate')
    time_diffs = df_sorted['InvoiceDate'].diff() #Calcilating difference between consectutive transactions

    max_gap = time_diffs.max()
    logger.info(f'Logest gap between transactions: {max_gap}')
    return max_gap


#
def check_cancellations(df):
    df['Invoice_Str'] = df['Invoice'].astype(str)

    bad_cancellations = df[(df['Invoice_Str'].str.startswith('C', na=False)) & (df['Quantity']>0)]

    if not bad_cancellations.empty:
        logger.error(f'Critical: found {len(bad_cancellations)} cancellations with Positive Quantity')

    else:
        logger.info('Logic Check: All cancellations have negative quantities')


def check_outliers(df):
    Q1 = df['Quantity'].quantile(0.25)
    Q3 = df['Quantity'].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df['Quantity']<lower_bound )| (df['Quantity']>upper_bound)]

    logger.info(f'Outlier Detection: found {len(outliers)} rows outside typical Quantity range')
    logger.info(f'Extreme threshold: > {upper_bound:.2f} units')

    return outliers

def check_geographic_breadth(df):
    price_variance = df.groupby('Country')['Price'].var().sort_values(ascending=False)
    logger.info(f'Top  countries by Price Variance:\n {price_variance.head()}')
    return price_variance

def check_ghost_customers(df):
    null_customers = df['Customer ID'].isnull().sum()
    logger.info(f'Ghost Customers: {null_customers} rows {null_customers/len(df):.1f}% have no ID')

    temp_rev = df['Quantity'] * df['Price']

    avg_reg = temp_rev[df['Customer ID'].notnull()].mean()
    avg_ghost = temp_rev[df['Customer ID'].isnull()].mean()

    logger.info(f'Avg Spend: Registered = {avg_reg:.2f}, Guest={avg_ghost:.2f}')

def run_all_checks(df):
    logger.info('--- Starting Exploratory Data Integrity (EDI) ---')
    check_uniques(df)
    check_zero_prices(df)
    check_description_consistency(df)
    check_temporal_gaps(df)
    check_cancellations(df)
    check_outliers(df)
    check_geographic_breadth(df)
    check_ghost_customers(df)
    logger.info('--- EDI Complete ---')


if __name__ == '__main__':
    from src.ingestion import load_and_optimize_data
    df = load_and_optimize_data()
    if df is not None:
        run_all_checks(df)






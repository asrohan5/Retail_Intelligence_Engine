import pandas as pd
import numpy as np

def engineer_features(df_clean, df_raw):

    ref_date = df_clean['InvoiceDate'].max()
    
    features = df_clean.groupby('Customer ID').agg({
        'InvoiceDate': lambda x: (ref_date - x.max()).days,
        'Invoice': 'nunique',
        'TotalAmount': 'sum'
    }).rename(columns={
        'InvoiceDate': 'recency',
        'Invoice': 'frequency',
        'TotalAmount': 'monetary'
    })

   
    recent_mask = df_clean['InvoiceDate'] > (ref_date - pd.Timedelta(days=30))
    prior_mask = (df_clean['InvoiceDate'] <= (ref_date - pd.Timedelta(days=30))) & \
                 (df_clean['InvoiceDate'] > (ref_date - pd.Timedelta(days=60)))
    
    spend_recent = df_clean[recent_mask].groupby('Customer ID')['TotalAmount'].sum()
    spend_prior = df_clean[prior_mask].groupby('Customer ID')['TotalAmount'].sum()
    
    features['spend_last_30d'] = spend_recent.reindex(features.index, fill_value=0)
    features['spend_prior_30d'] = spend_prior.reindex(features.index, fill_value=0)
 
    features['spend_velocity'] = features['spend_last_30d'] / features['spend_prior_30d'].replace(0, 1)


    df_sorted = df_clean.sort_values(['Customer ID', 'InvoiceDate'])

    df_sorted['days_diff'] = df_sorted.groupby('Customer ID')['InvoiceDate'].diff().dt.days
    features['purchase_interval_std'] = df_sorted.groupby('Customer ID')['days_diff'].std().fillna(0)


    df_clean['category_proxy'] = df_clean['StockCode'].astype(str).str[:3]
    
    diversity_metrics = df_clean.groupby('Customer ID').agg({
        'StockCode': 'nunique',      
        'category_proxy': 'nunique'   
    }).rename(columns={'StockCode': 'unique_products', 'category_proxy': 'unique_categories'})
    
    features = features.join(diversity_metrics)



    df_clean['is_weekend'] = df_clean['InvoiceDate'].dt.dayofweek >= 5
    weekend_counts = df_clean.groupby('Customer ID')['is_weekend'].mean()
    features['weekend_ratio'] = weekend_counts


    features['avg_unit_price'] = df_clean.groupby('Customer ID')['Price'].mean()


    global_avg_qty = df_clean['Quantity'].mean()
    user_avg_qty = df_clean.groupby('Customer ID')['Quantity'].mean()
    features['whale_score'] = user_avg_qty / global_avg_qty

    
    raw_filtered = df_raw[df_raw['Customer ID'].isin(features.index)]
    
    total_inv = raw_filtered.groupby('Customer ID')['Invoice'].nunique()
    cancel_inv = raw_filtered[raw_filtered['Invoice'].astype(str).str.startswith('C', na=False)] \
                             .groupby('Customer ID')['Invoice'].nunique()
    
    features['return_rate'] = (cancel_inv.reindex(features.index, fill_value=0) / 
                               total_inv.reindex(features.index, fill_value=1)).fillna(0)


    features['avg_hour'] = df_clean.groupby('Customer ID')['InvoiceDate'].apply(lambda x: x.dt.hour.mean())

    return features
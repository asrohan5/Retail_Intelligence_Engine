import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

def clean_data_for_metrics(df):

    initial_count = len(df)

    df_clean = df.dropna(subset=['Customer ID']).copy()

    df_clean = df_clean[~df_clean['Invoice'].astype(str).str.startswith('C')]

    df_clean = df_clean[df_clean['Price']>0]

    df_clean['TotalAmount'] = df_clean['Quantity'] * df_clean['Price']

    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])

    logger.info(f'Data Cleaning: {initial_count} -> {len(df_clean)}')

    return df_clean


def calculate_rfm_values(df):
    reference_date = df['InvoiceDate'].max() + pd.Timedelta(days=1)

    rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda x: (reference_date - x.max()).days,
                                         'Invoice':'nunique',
                                           'TotalAmount':'sum'}).reset_index()
    
    rfm.rename(columns={'InvoiceDate':'Recency', 'Invoice':'Frequency','TotalAmount':'Monetary'}, inplace=True)



    
    return rfm


def assign_rfm_scores(rfm_df):
    labels = [1,2,3,4,5]
    
    rfm_df['R_score'] = pd.qcut(rfm_df['Recency'], q=5, labels = list(reversed(labels)))

    rfm_df['F_score'] = pd.qcut(rfm_df['Frequency'].rank(method='first'), q=5, labels=labels)

    rfm_df['M_score'] = pd.qcut(rfm_df['Monetary'], q=5, labels = labels)

    rfm_df['Segment'] = rfm_df['R_score'].astype(str) + \
                        rfm_df['F_score'].astype(str) + \
                        rfm_df['M_score'].astype(str)

    return rfm_df


def define_customer_segments(rfm_df):

    def segment_logic(row):
        r,f,m = int(row['R_score']), int(row['F_score']), int(row['M_score'])

        if r >= 5 and f>=5 and m>=5:
            return "Champions"
        elif f>=4:
            return "Loyalists"
        elif r<=2 and f>=4:
            return "At Risk"
        elif r>=4 and f==1:
            return "New Customers"
        elif r<=2 and f<=2:
            return "Hibernating"
        else:
            return "Potential Loyalist"
        
    rfm_df['Segment'] = rfm_df.apply(segment_logic, axis=1)
    return rfm_df

def calculate_cohort_index(df):
    df['InvoiceMonth'] = df['InvoiceDate'].apply(lambda x: x.replace(day=1).date())
    group = df.groupby('Customer ID')['InvoiceMonth']
    df['CohortMonth'] = group.transform('min')

    invoice_year = pd.to_datetime(df['InvoiceMonth']).dt.year
    invoice_month = pd.to_datetime(df['InvoiceMonth']).dt.month
    cohort_year = pd.to_datetime(df['CohortMonth']).dt.year
    cohort_month = pd.to_datetime(df['CohortMonth']).dt.month

    years_diff = invoice_year - cohort_year
    month_diff = invoice_month - cohort_month

    df['CohortIndex'] = years_diff * 12 + month_diff + 1

    return df

def get_retention_matrix(df):
    cohort_data = df.groupby(['CohortMonth', 'CohortIndex'])['Customer ID'].nunique().reset_index()

    cohort_pivot = cohort_data.pivot(index='CohortMonth', columns='CohortIndex', values='Customer ID')
    cohort_size = cohort_pivot.iloc[:, 0]

    retention_matrix = cohort_pivot.divide(cohort_size, axis = 0)

    return retention_matrix


def calculate_monthly_aov(df):
    monthly = df.groupby('InvoiceMonth').agg({'TotalAmount':'sum', 'Invoice':'nunique'})

    monthly['AOV'] = monthly['TotalAmount']/monthly['Invoice']
    return monthly['AOV']

def calculate_new_vs_repeat(df):
    first_purchase = df.groupby('Customer ID')['Invoice Date'].min().reset_index()
    first_purchase.columns = ['Customer ID', 'FirstPurchaseDate']

    df = df.merge(first_purchase, on='Customer ID')

    df['UserType'] = np.where(df['InvoiceDate'] == df['FirstPurchaseDate'], 'New', 'Repeat')

    return df.groupby(['InvoiceMonth', 'UserType'])['Customer ID'].nunique().unstack()

def calculate_churn_risk(df, days_threshold = 90):
    max_date = df['InvoiceDate'].max()

    last_purchase = df.groupby('Customer ID').agg({'InvoiceDate':'max', 'TotalAmount':'sum'}).reset_index()

    last_purchase['DaysDormant'] = (max_date - last_purchase['InvoiceDate']).dt.days

    churn_risk = last_purchase[last_purchase['DaysDormant'] > days_threshold]

    logger.warning(f'Churn Risk: {len(churn_risk)} user dormant>{days_threshold} days')
    logger.warning(f'Potential Revenue at Risk: {churn_risk['TotalAmount'].sum():.2f}')

    return churn_risk

def build_executive_summary(df):

    aov = calculate_monthly_aov(df)
    monthly_rev = df.groupby('InvoiceMonth')['TotalAmount'].sum()
    growth_pct = monthly_rev.pct_change() * 100

    active_users = df.groupby('InvoiceMonth')['Customer ID'].nunique()

    summary = pd.DataFrame({'Revenue':monthly_rev, 'Growth_Pct':growth_pct, 'Active_Users':active_users, 'AOV':aov})

    return summary.round(2)




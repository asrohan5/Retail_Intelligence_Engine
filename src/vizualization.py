import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

PLOT_PATH = os.path.join('plots')
os.makedirs(PLOT_PATH, exist_ok=True)

def plot_retention_heatmap(retention_matrix):
    plt.figure(figsize=(12,8))
    plt.title('Customer Retention Rate (Monthly Cohorts)', fontsize = 16)

    sns.heatmap(retention_matrix, annot=True, fmt='.0%', cmap='Blues', cbar_kws={'label':'Retention Rate'})

    plt.xlabel('Cohort Index (Months)')
    plt.ylabel('Cohort Month')

    save_to = os.path.join(PLOT_PATH, '1_Customer_Retention_Rate.png')
    plt.savefig(save_to)

    plt.show()


def plot_segement_distribution(rfm_df):
    plt.figure(figsize=(12,8))
    plt.title('Customer Segmentation Distribution', fontsize=14)

    segment_data=rfm_df.groupby('Segment').agg({'Customer ID': 'count', 'Monetary': 'mean'}).sort_values('Customer ID' ,ascending=False).reset_index()
  

    sns.barplot(data=segment_data, x='Customer ID', y='Segment', palette='viridis')

    plt.xlabel('No. of Customers')
    plt.ylabel('Market Segment')
    plt.tight_layout()

    save_to = os.path.join(PLOT_PATH, '2_Customer_Segmentation_Distribution.png')
    plt.savefig(save_to)

    plt.show()

def plot_revenue_growth(exec_summary):
    plot_df = exec_summary.iloc[:-1].copy()
    fig, ax1 = plt.subplots(figsize=(12,6))

    ax1.set_title('Monthly Revenue and Growth Velocity')
    sns.barplot(x=plot_df.index, y=plot_df['Revenue'], ax = ax1, color = 'skyblue', alpha = 0.7)
    ax1.set_ylabel('Total Revenue')
    ax1.tick_params(axis='x', rotation=45)

    ax2=ax1.twinx()
    sns.lineplot(x=np.arange(len(plot_df)), y=plot_df['Growth_Pct'], ax=ax2, color='red', marker='o', linewidth=2)
    ax2.set_ylabel('Month over month growth in %')
    plt.tight_layout()

    save_to = os.path.join(PLOT_PATH, '3_Monthly_Revenue_Growth_Velocity.png')
    plt.savefig(save_to)

    plt.show()

def plot_product_performance(df):
    prof_perf = df.groupby('Description').agg({'Quantity':'sum', 'Price': 'mean'}).reset_index()

    prod_perf = prod_perf.sort_values('Quantity', ascending=False).head(100)

    plt.figure(figsize=(10,6))
    sns.scatterplot(data=prod_perf, x='Quantity', y='Price', alpha=0.6, size='Quantity', sizes=(20,200))

    plt.title('Top 100 Products: Volume v Unit Price')
    plt.xscale('log')
    plt.grid(True, which='both', ls="-", alpha=0.2)

    save_to = os.path.join(PLOT_PATH, '4_Volume_v_Unit_price.png')
    plt.savefig(save_to)

    plt.show()


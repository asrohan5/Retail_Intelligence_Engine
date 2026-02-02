import logging
from src.ingestion import load_and_optimize_data
from src.metrics import *
from src import vizualization as viz
from src import features  # Import the new module

logging.basicConfig(level=logging.INFO, format = "%(asctime)s [%(levelname)s] %(message)s")

def run_pipeline():

    df_raw = load_and_optimize_data()
    if df_raw is None:
        logging.error('Pipeline failed: Could not load data')
        return

    df = clean_data_for_metrics(df_raw)

    logging.info('Generating RFM Segments')
    rfm = calculate_rfm_values(df)
    rfm = assign_rfm_scores(rfm)
    rfm = define_customer_segments(rfm)


    logging.info('Calculating Cohort Retention')
    df_cohort = calculate_cohort_index(df)
    retention = get_retention_matrix(df_cohort)


    logging.info('Building Executive Summary')
    exec_summary = build_executive_summary(df)


    logging.info('Preparing Vizualizations')
    viz.plot_retention_heatmap(retention)
    viz.plot_segement_distribution(rfm)
    viz.plot_revenue_growth(exec_summary)

    logging.info('Pipeline Execution Completed')



    logging.info("Engineering Predictive Features...")
    feature_matrix = features.engineer_features(df, df_raw)
    

    print("\n--- Day 6 Feature Matrix Sample ---")
    print(feature_matrix[['spend_velocity', 'return_rate', 'whale_score']].head())
    print(f"Total Features Generated: {feature_matrix.shape[1]}")
    print("\n\n")


    feature_matrix.to_csv("outputs/feature_matrix.csv")

if __name__ == "__main__":
    run_pipeline()
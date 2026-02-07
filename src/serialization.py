import joblib
import os
import logging

def save_production_artifacts(model, scaler, feature_columns):

    os.makedirs('models', exist_ok=True)

    artifacts = {
        'model':model, 
        'scaler':scaler,
        'features':feature_columns
    }

    joblib.dump(artifacts, 'models/retail_churn_v1.pkl')
    logging.info("model artifacts saved :::")

def load_production_model():
    if not os.path.exists('models/retail_churn_v1.pkl'):
        raise FileNotFoundError("no production model found")
    

    logging.info(f'loading model from model/')
    artifacts= joblib.load('models/retail_churn_v1.pkl')
    return artifacts

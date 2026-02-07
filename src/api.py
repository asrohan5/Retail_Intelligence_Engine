from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import uvicorn
from src.serialization import load_production_model

app = FastAPI(title="112 Retail Churn API", version="1.0")

try:
    artifacts=load_production_model()
    model = artifacts['model']
    scaler = artifacts['scaler']
    required_features = artifacts['features']
    print('Model Loaded Successfully')

except Exception as e:
    print(f'Model Failed to Load: {e}')
    model = None


#Defining Input Schema: exact input formats
class CustomerState(BaseModel):
    recency: float
    frequency: float
    monetary: float
    spend_velocity: float
    purchase_interval_std: float
    unique_products: int
    unique_categories: int
    weekend_ratio: float
    avg_unit_price: float
    whale_score: float
    return_rate: float
    avg_hour: float


#Prediction
@app.post("/prediction_churn")

def predict(customer: CustomerState):
    if not model:
        print("CRITICAL ERROR: Model Variable is None inside endpoint")
        raise HTTPException(status_code=500, detail='Model is not Loaded')
    
    input_data = pd.DataFrame([customer.model_dump()]) #Converting incoming JSON into DF

    try:
        input_data = input_data[required_features]
    except KeyError as e:
        raise HTTPException(statud_code=400, detail=f'Missing Feature: {e}')
    
    scaled_data = scaler.transform(input_data)
    prediction = model.predict(scaled_data)[0]
    probability = model.predict_proba(scaled_data)[0][1]
    return {
        'customer_id': "input_user",
        'churn_prediction': int(prediction),
        'churn_probability': float(probability),
        'risk_level': "CRITICAL" if probability > 0.7 else "Normal"
    }



#Health Check
@app.get("/health")
def health_check():
    return {'status': "active", "model_version": "v1.0"}

if __name__ == "__main__":
    uvicorn.run("src.api:app", host='0.0.0.0', port=8000, reload=True)




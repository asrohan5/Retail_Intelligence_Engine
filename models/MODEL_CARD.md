# Model Card: Retail Churn Predictor v1.0

## Model Details
- **Type:** Random Forest Classifier
- **Task:** Binary Churn Prediction (90-day window)
- **Features used:** Recency, Frequency, Monetary, Whale Score, Spend Velocity.

## Performance
- **ROC-AUC:** 0.7623
- **Precision (Churn):** 0.66
- **Recall (Churn):** 0.71

## Intent & Usage
This model is served via FastAPI to identify high-risk wholesale customers. 
**Threshold recommendation:** 0.70 for automated email triggers; 0.50 for manual sales review.
# Retail Intelligence Engine: Predictive Churn System


## Business Overview
A UK-based wholesaler faced declining customer retention. This project provides an end-to-end ML solution to predict which wholesale customers are likely to churn in the next 90 days, allowing for proactive retention campaigns.

## Tech Stack
- **Engine:** Python 3.13, Pandas (Memory Optimized)
- **Modeling:** Scikit-Learn (Random Forest + GridSearch)
- **Deployment:** FastAPI (REST API)
- **MLOps:** Pytest for Unit Testing, GitHub Actions for CI/CD

## Key Insights
- **Whale Score:** High-volume customers show higher volatility.
- **Spend Velocity:** A sudden drop in purchasing frequency is the #1 predictor of churn.
- **Model Performance:** Achieved an ROC-AUC of **0.76**, balancing precision and recall to minimize "false alarms" for the marketing team.

## Deployment
1. **Clone & Install:** `pip install -r requirements.txt`
2. **Run API:** `python -m src.api`
3. **Run Tests:** `pytest`





from app.model import predict_churn
from app.schemas import CustomerFeatures
from fastapi import FastAPI

app = FastAPI(title="Customer Churn Prediction API")


@app.get("/")
def home():

    return {"message": "Churn API is running"}


@app.post("/predict")
def predict(customer: CustomerFeatures):

    features = [
        customer.frequency,
        customer.monetary,
        customer.recency,
        customer.avg_order_value,
    ]

    result = predict_churn(features)

    return result

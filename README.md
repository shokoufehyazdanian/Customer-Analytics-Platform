# Customer Analytics Platform

End-to-End Data Analytics & Machine Learning Platform

This project demonstrates an end-to-end analytics platform
built with modern data engineering, analytics and machine learning tools.

The goal is to analyze customer behavior, generate business insights,
and predict customer churn.
## Business Problem

E-commerce companies need to understand:

- Which customers generate the most value?
- Which products drive revenue?
- Which customers are at risk of churn?
- How can data support business decisions?

This project builds a complete analytics pipeline
to answer these questions.


## Architecture

```mermaid
flowchart TD
    A[Data Source] --> B[Python ETL]
    B --> C[PostgreSQL]
    C --> D[Great Expectations]
    D --> E[dbt Warehouse]
    E --> F[Power BI Dashboard]
    F --> G[ML Pipeline]
    G --> H[FastAPI]
```

## Tech Stack

### Data Engineering

- Python
- PostgreSQL
- Docker
- dbt
- Great Expectations


### Analytics

- SQL
- Pandas
- Power BI


### Machine Learning

- Scikit-learn
- XGBoost
- MLflow


### Deployment

- FastAPI
- Docker
- GitHub Actions

## Project Structure


customer-analytics-platform/

```text
.
├── data
│   └── raw
│       └── dataset files
│
├── data_loader
│   ├── Dockerfile
│   ├── requirements.txt
│   └── load_data.py
│
├── src
│   └── data ingestion
│
├── customer_analytics_dbt
│   └── transformation models
│
├── ml
│   ├── feature engineering
│   ├── training
│   └── models
│
├── api
│   └── FastAPI service
│
├── dashboard
│   └── Power BI dashboard
│
└── docker-compose.yml
```
## Data Pipeline


1. Data ingestion

Raw datasets are loaded into PostgreSQL using a dedicated Docker data loader service.

The loader reads CSV files from:

data/raw/

Expected files:

data/raw/

├── olist_orders_dataset.csv
├── olist_order_items_dataset.csv
├── olist_products_dataset.csv
└── olist_order_reviews_dataset.csv

The data_loader container automatically imports these files into PostgreSQL.

2. Data validation

Great Expectations validates data quality.


3. Data transformation

dbt creates analytical models.


4. Analytics

Business KPIs are generated.


5. Machine Learning

Customer churn prediction model is trained.

## Dashboard Preview


### Executive Overview

![Dashboard](dashboard/screenshots/dashboard.png)

### Products 

![Products](dashboard/screenshots/products.png)

## Machine Learning Model


### Problem

Customer churn prediction.


### Features

- Recency
- Frequency
- Monetary Value
- Average Order Value


### Models Tested

- Logistic Regression
- Random Forest
- XGBoost


### Evaluation Metrics

- Accuracy
- Precision
- Recall
- ROC-AUC

Best Model:

Random Forest

ROC-AUC:
0.67


## How To Run


Clone repository:

git clone [REPOSITORY](https://github.com/shokoufehyazdanian/Customer-Analytics-Platform)

Dataset Setup:

Raw datasets are not included in this repository because of their size.

Download the Brazilian E-Commerce Public Dataset by Olist from Kaggle:

https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

After downloading, extract the CSV files into:

data/raw/

After placing the files, Docker will automatically load them into PostgreSQL.

Create environment:

python -m venv venv


Install dependencies:

pip install -r requirements.txt


Start services:

docker compose up -d


Run dbt:

cd customer_analytics_dbt

dbt run


Start API:

uvicorn api.app.main:app --reload

## Future Improvements


- Cloud deployment (AWS/Azure)
- Data warehouse migration
- Real-time streaming pipeline
- Advanced ML monitoring
- Automated retraining

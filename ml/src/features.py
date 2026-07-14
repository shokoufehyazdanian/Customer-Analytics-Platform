import pandas as pd
from config import DATABASE_URL
from sqlalchemy import create_engine


def load_customer_data():

    engine = create_engine(DATABASE_URL)

    query = """

    SELECT *

    FROM public_analytics.mart_customer_rfm

    """

    df = pd.read_sql(query, engine)

    return df


def create_features(df):

    features = df.copy()

    return features


if __name__ == "__main__":

    df = load_customer_data()

    df = create_features(df)

    df.to_csv("ml/data/training/customer_churn.csv", index=False)

    print(df.head())

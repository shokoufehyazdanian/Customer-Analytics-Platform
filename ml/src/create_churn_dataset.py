import pandas as pd
from config import DATABASE_URL
from sqlalchemy import create_engine

# -----------------------------
# Configuration
# -----------------------------

SNAPSHOT_DATE = pd.Timestamp("2017-11-01")

OUTPUT_PATH = "ml/data/training/customer_churn.csv"


# -----------------------------
# Load Data
# -----------------------------


def load_orders():

    engine = create_engine(DATABASE_URL)

    query = """

    SELECT

        c.customer_unique_id,

        o.order_id,

        o.order_purchase_timestamp,

        p.payment_value

    FROM public.olist_orders_dataset o

    JOIN public.olist_customers_dataset c

        ON o.customer_id = c.customer_id

    JOIN public.olist_order_payments_dataset p

        ON o.order_id = p.order_id

    WHERE o.order_status = 'delivered'

    """

    df = pd.read_sql(query, engine)

    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

    return df


# -----------------------------
# Feature Engineering
# -----------------------------
def create_features(df):

    past_orders = df[df["order_purchase_timestamp"] < SNAPSHOT_DATE].copy()

    features = (
        past_orders.groupby("customer_unique_id")
        .agg(
            frequency=("order_id", "count"),
            monetary=("payment_value", "sum"),
            last_purchase_date=("order_purchase_timestamp", "max"),
        )
        .reset_index()
    )

    features["recency"] = (SNAPSHOT_DATE - features["last_purchase_date"]).dt.days

    features["avg_order_value"] = features["monetary"] / features["frequency"]

    # Only repeat customers

    features = features[features["frequency"] >= 2].copy()

    return features


# -----------------------------
# Create Target
# -----------------------------


def create_target(features, df):

    future_end = SNAPSHOT_DATE + pd.Timedelta(days=180)

    future_orders = df[
        (df["order_purchase_timestamp"] >= SNAPSHOT_DATE)
        & (df["order_purchase_timestamp"] < future_end)
    ]

    active_customers = set(future_orders["customer_unique_id"])

    features["churn"] = (~features["customer_unique_id"].isin(active_customers)).astype(
        int
    )

    return features


# -----------------------------
# Main
# -----------------------------


def main():

    print("Loading orders...")

    orders = load_orders()

    print(f"Orders loaded: {len(orders):,}")

    print("Creating features...")

    features = create_features(orders)

    print("Creating target...")

    dataset = create_target(features, orders)

    print("\nChurn distribution:")

    print(dataset["churn"].value_counts())

    print("\nDataset preview:")

    print(dataset.head())

    dataset.to_csv(OUTPUT_PATH, index=False)

    print("\nDataset saved to:", OUTPUT_PATH)


if __name__ == "__main__":

    main()

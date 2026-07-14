import joblib
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split

DATA_PATH = "ml/data/training/customer_churn.csv"

MODEL_PATH = "ml/models/churn_model.pkl"


df = pd.read_csv(DATA_PATH)


X = df[
    [
        "frequency",
        "monetary",
        "avg_order_value",
        "customer_lifetime_days",
    ]
]

y = df["churn"]


mlflow.set_experiment("customer_churn_prediction")


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42,
)


with mlflow.start_run(run_name="random_forest_v1"):

    model.fit(
        X_train,
        y_train,
    )

    predictions = model.predict(X_test)

    probability = model.predict_proba(X_test)[:, 1]

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    auc = roc_auc_score(
        y_test,
        probability,
    )

    mlflow.log_param(
        "model",
        "RandomForest",
    )

    mlflow.log_param(
        "features",
        ",".join(X.columns),
    )

    mlflow.log_metric(
        "accuracy",
        accuracy,
    )

    mlflow.log_metric(
        "roc_auc",
        auc,
    )

    mlflow.sklearn.log_model(
        model,
        "model",
    )


joblib.dump(
    model,
    MODEL_PATH,
)


print("Model saved")

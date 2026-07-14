import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import (ConfusionMatrixDisplay, classification_report,
                             confusion_matrix, roc_auc_score, roc_curve)

DATA_PATH = "ml/data/training/customer_churn.csv"


MODEL_PATH = "ml/models/churn_model.pkl"


# Load data
df = pd.read_csv(DATA_PATH)


# Load model
model = joblib.load(MODEL_PATH)


features = ["frequency", "monetary", "avg_order_value", "customer_lifetime_days"]


X = df[features]

y = df["churn"]


# Prediction
predictions = model.predict(X)

probabilities = model.predict_proba(X)[:, 1]


# ==========================
# Metrics
# ==========================

auc = roc_auc_score(y, probabilities)


print("ROC-AUC:", auc)


print(classification_report(y, predictions))


# ==========================
# Confusion Matrix
# ==========================

cm = confusion_matrix(y, predictions)


display = ConfusionMatrixDisplay(confusion_matrix=cm)


display.plot()

plt.title("Churn Confusion Matrix")

plt.show()


# ==========================
# ROC Curve
# ==========================

fpr, tpr, thresholds = roc_curve(y, probabilities)


plt.figure()

plt.plot(fpr, tpr)


plt.xlabel("False Positive Rate")


plt.ylabel("True Positive Rate")


plt.title("Churn ROC Curve")


plt.show()


# ==========================
# Feature Importance
# ==========================

importance = pd.DataFrame(
    {"feature": features, "importance": model.feature_importances_}
)


importance = importance.sort_values(by="importance", ascending=False)


print("\nFeature Importance:")


print(importance)

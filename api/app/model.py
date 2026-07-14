import joblib


MODEL_PATH = "ml/models/churn_model.pkl"


model = joblib.load(MODEL_PATH)


def predict_churn(features):

    prediction = model.predict(
        [features]
    )

    probability = model.predict_proba(
        [features]
    )[0][1]


    return {
        "prediction": int(prediction[0]),
        "churn_probability": float(probability)
    }
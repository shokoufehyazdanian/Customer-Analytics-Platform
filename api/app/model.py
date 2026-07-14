from pathlib import Path

import joblib

MODEL_PATH = Path(__file__).parent.parent / "models" / "churn_model.pkl"

model = None


def get_model():

    global model

    if model is None:
        model = joblib.load(MODEL_PATH)

    return model


def predict_churn(features):

    model = get_model()

    prediction = model.predict([features])

    return {"prediction": int(prediction[0])}

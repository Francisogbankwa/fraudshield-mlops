from fastapi import FastAPI
from pathlib import Path
import json
import joblib
import pandas as pd
from fastapi import HTTPException
from pydantic import BaseModel, Field
from functools import lru_cache

app = FastAPI(
    title="FraudShield AI",
    description="Credit card fraud detection API",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "FraudShield AI",
    }
ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"


@lru_cache(maxsize=1)
def load_model():
    return joblib.load(MODEL_DIR / "fraud_model.joblib")

@lru_cache(maxsize=1)
def load_threshold():
    with open(MODEL_DIR / "threshold.json") as file:
        return json.load(file)["threshold"]
model = load_model()
threshold = load_threshold()
class Transaction(BaseModel):
    Time: float
    Amount: float = Field(ge=0)
    features: list[float] = Field(min_length=28, max_length=28) 
@app.post("/predict")
def predict(transaction: Transaction):
    model = load_model()
    threshold = load_threshold()

    columns = ["Time"] + [
        f"V{i}" for i in range(1, 29)
    ] + ["Amount"]

    values = (
        [transaction.Time]
        + transaction.features
        + [transaction.Amount]
    )

    data = pd.DataFrame([values], columns=columns)

    try:
        probability = float(model.predict_proba(data)[0][1])
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Model prediction failed"
        )

    prediction = int(probability >= threshold)

    return {
        "fraud_probability": probability,
        "fraud_prediction": prediction,
        "threshold": threshold,
    }

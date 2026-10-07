from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import tensorflow as tf
from fastapi import FastAPI
from pydantic import BaseModel, Field


BASE_DIR = Path(__file__).resolve().parent

# Load trained models and scaler
burnout_model = tf.keras.models.load_model(BASE_DIR / "burnout_model.keras")
mental_model = tf.keras.models.load_model(BASE_DIR / "mental_health_model.keras")
scaler = joblib.load(BASE_DIR / "scaler.save")

FEATURES = [
    "stress_level",
    "anxiety_score",
    "depression_score",
    "exam_pressure",
    "sleep_hours",
    "study_hours_per_day",
    "financial_stress",
    "family_expectation",
    "social_support",
    "physical_activity",
]

BURNOUT_LABELS = {
    0: "Low",
    1: "Medium",
    2: "High",
}

MENTAL_LABELS = {
    0: "Buruk",
    1: "Sedang",
    2: "Baik",
}


class PredictionInput(BaseModel):
    stress_level: float = Field(..., description="Stress level")
    anxiety_score: float = Field(..., description="Anxiety score")
    depression_score: float = Field(..., description="Depression score")
    exam_pressure: float = Field(..., description="Exam pressure")
    sleep_hours: float = Field(..., description="Sleep hours")
    study_hours_per_day: float = Field(..., description="Study hours per day")
    financial_stress: float = Field(..., description="Financial stress")
    family_expectation: float = Field(..., description="Family expectation")
    social_support: float = Field(..., description="Social support")
    physical_activity: float = Field(..., description="Physical activity")


app = FastAPI(
    title="Burniva AI API",
    description="API untuk prediksi risiko burnout dan kategori kesehatan mental mahasiswa.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Burniva AI API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: PredictionInput):
    # Keep the exact feature order used during model training.
    input_df = pd.DataFrame(
        [[getattr(data, feature) for feature in FEATURES]],
        columns=FEATURES,
    )

    input_scaled = scaler.transform(input_df)

    burnout_prob = burnout_model.predict(input_scaled, verbose=0)[0]
    mental_prob = mental_model.predict(input_scaled, verbose=0)[0]

    burnout_class = int(np.argmax(burnout_prob))
    mental_class = int(np.argmax(mental_prob))

    return {
        "burnout": {
            "class": burnout_class,
            "label": BURNOUT_LABELS[burnout_class],
            "confidence": float(burnout_prob[burnout_class]),
            "probabilities": {
                BURNOUT_LABELS[i]: float(prob)
                for i, prob in enumerate(burnout_prob)
            },
        },
        "mental_health": {
            "class": mental_class,
            "label": MENTAL_LABELS[mental_class],
            "confidence": float(mental_prob[mental_class]),
            "probabilities": {
                MENTAL_LABELS[i]: float(prob)
                for i, prob in enumerate(mental_prob)
            },
        },
    }

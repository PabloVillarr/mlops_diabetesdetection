from fastapi import FastAPI
import uvicorn
import pickle
import pandas as pd

# ========= Carga de artefactos =========
app = FastAPI()
modelo = pickle.load(open("diabetes_model.pkl", "rb"))

# Orden de columnas que espera el modelo
columnas = [
    "Gender", "AGE", "Urea", "Cr", "HbA1c",
    "Chol", "TG", "HDL", "LDL", "VLDL", "BMI"
]

# Mapeo de clases
CLASES_MAP = {
    0: "Non-Diabetic",
    1: "Diabetic",
    2: "Prediabetic"
}

# ========= Helper =========
def model_pred(features_dict: dict) -> int:
    df = pd.DataFrame([features_dict], columns=columnas)
    pred = modelo.predict(df)
    return int(pred[0])

def model_proba(features_dict: dict) -> dict:
    df = pd.DataFrame([features_dict], columns=columnas)
    proba = modelo.predict_proba(df)[0]  # array de probabilidades
    return {CLASES_MAP[int(cls)]: float(prob) for cls, prob in zip(modelo.classes_, proba)}

# ========= Endpoints =========
@app.get("/")
async def root():
    return {"message": "Prediction"}

@app.get("/predict")
async def predict(
    Gender: int,
    AGE: int,
    Urea: float,
    Cr: float,
    HbA1c: float,
    Chol: float,
    TG: float,
    HDL: float,
    LDL: float,
    VLDL: float,
    BMI: float,
):
    # Armar features en el orden exacto
    features = {
        "Gender": Gender,
        "AGE": AGE,
        "Urea": Urea,
        "Cr": Cr,
        "HbA1c": HbA1c,
        "Chol": Chol,
        "TG": TG,
        "HDL": HDL,
        "LDL": LDL,
        "VLDL": VLDL,
        "BMI": BMI,
    }

    pred = model_pred(features)
    etiqueta = CLASES_MAP.get(pred, "Unknown")
    proba_dict = model_proba(features)

    mensajes = {
        0: "Non-diabetic. No worries :)",
        1: "Diabetic.",
        2: "Prediabetic."
    }

    return {
        "class_id": pred,
        "class_name": etiqueta,
        "message": mensajes.get(pred, "Unknown"),
        "probabilities": proba_dict
    }

"""
# Para ejecutar local:
if __name__ == "__main__":
    uvicorn.run(app, port=8080, host="0.0.0.0")
"""


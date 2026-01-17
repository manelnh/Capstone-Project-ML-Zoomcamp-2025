import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

# Load model and DictVectorizer
with open("model_rfr.bin", "rb") as f_in:
    rf_model, dv = pickle.load(f_in)

class ESGData(BaseModel):
    # Raw categorical features as strings
    sector: str
    industry: str
    controversy_level: str
    esg_risk_level: str

    # Numerical features
    environment_risk_score: float
    governance_risk_score: float
    social_risk_score: float
    controversy_score: float

class PredictionResponse(BaseModel):
    total_esg_risk_score: float

app = FastAPI()

def preprocess_input(data: ESGData) -> pd.DataFrame:
    # Convert Pydantic model to dict
    data_dict = data.dict()

    # Use DictVectorizer: expects list of dicts with raw categorical + numerical features
    X = dv.transform([data_dict])
    return pd.DataFrame(X, columns=dv.get_feature_names_out())

@app.post("/predict", response_model=PredictionResponse)
async def predict(data: ESGData):
    X = preprocess_input(data)
    pred = rf_model.predict(X)[0]
    return PredictionResponse(total_esg_risk_score=round(float(pred), 4))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

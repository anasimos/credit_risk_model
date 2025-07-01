# src/api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib # For loading the model
import os
import mlflow # For MLflow Model Registry integration (though we'll use joblib for simplicity first)
from src.api.pydantic_models import CustomerFeatures, PredictionResponse # Import our Pydantic models

# Initialize FastAPI app
app = FastAPI(
    title="Bati Bank Credit Risk Prediction API",
    description="API for predicting credit risk of customers based on transactional behavior.",
    version="1.0.0"
)

# --- Model Loading ---
# In a real MLflow setup, you'd use mlflow.pyfunc.load_model or mlflow.sklearn.load_model
# For this challenge, we'll simulate loading a trained model.
# We need to save our trained RandomForestClassifier model first.

model = None # Placeholder for our loaded model
# Define the path where the model will be saved (e.g., in a 'models' directory)
MODEL_PATH = "models/random_forest_credit_risk_model.joblib"

@app.on_event("startup")
async def load_model():
    """
    Load the trained model when the FastAPI application starts up.
    """
    global model
    if not os.path.exists(MODEL_PATH):
        raise RuntimeError(f"Model file not found at {MODEL_PATH}. Please train and save the model first.")
    try:
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        raise RuntimeError(f"Could not load model from {MODEL_PATH}: {e}")

# --- Health Check Endpoint ---
@app.get("/health", summary="Health Check", response_model= dict[str, str])
async def health_check():
    """
    Checks if the API is running and the model is loaded.
    """
    if model is not None:
        return {"status": "ok", "model_loaded": "true"}
    else:
        return {"status": "error", "model_loaded": "false", "message": "Model not loaded"}

# --- Prediction Endpoint ---
@app.post("/predict", summary="Predict Credit Risk", response_model=PredictionResponse)
async def predict_credit_risk(customer_data: CustomerFeatures):
    """
    Accepts customer features and returns the predicted credit risk probability and label.
    """
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please check API health.")

    # Convert Pydantic model to pandas DataFrame for prediction
    # Ensure the order of columns matches the training data (X_train.columns)
    # This is CRUCIAL for correct predictions.
    # In a real scenario, you'd load X_train.columns and enforce that order.
    # For now, we'll assume the Pydantic model's fields are in the correct order
    # or handle it by creating a DataFrame from the dict.

    # Create a dictionary from the Pydantic model
    input_dict = customer_data.dict()
    # Convert to a DataFrame with a single row
    input_df = pd.DataFrame([input_dict])

    # IMPORTANT: Ensure column order matches X_train used during training
    # This is a placeholder. In a real app, you'd save X_train.columns
    # and reorder input_df to match.
    # For now, we'll rely on the Pydantic model's order.
    # If your model was trained on 69 features, the Pydantic model MUST have all 69.
    # And the order must match.
    # A robust solution involves saving the feature names during training and loading them here.
    # Example: X_train_columns = joblib.load('models/X_train_columns.joblib')
    # input_df = input_df[X_train_columns]

    try:
        # Predict probability (for class 1 - high risk)
        risk_probability = model.predict_proba(input_df)[:, 1][0]
        # Predict class label (0 or 1)
        risk_label = int(model.predict(input_df)[0])

        # Generate a dummy customer ID for response as we don't have it in input_df
        # In a real API, you might pass customer_id in the input_data or generate it.
        # For this challenge, let's use a placeholder or assume it's passed.
        # Let's add customer_id to CustomerFeatures Pydantic model if it's needed.
        # For now, let's just use a generic one or assume it's part of the input.
        # We need to add customer_id to CustomerFeatures if we want to return it.
        # Let's modify PredictionResponse to not require customer_id for simplicity
        # Or, if customer_id is part of the CustomerFeatures input, we can use it.
        # For now, let's assume customer_id is NOT part of the CustomerFeatures input
        # and just return a generic response.

        return PredictionResponse(
            customer_id="dummy_customer_id", # Placeholder
            risk_probability=float(risk_probability),
            risk_label=risk_label
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}. Ensure input features match model's expectations.")
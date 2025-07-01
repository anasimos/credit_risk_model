# src/api/pydantic_models.py

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

# Define the input schema for the /predict endpoint
# This should match the features your model expects in X_test
# For simplicity, we'll define a generic input that can be expanded.
# In a real scenario, you'd list all 69 features here with their types.

class CustomerFeatures(BaseModel):
    # Example: You would list all your 69 features here.
    # For demonstration, let's pick a few key ones.
    # In a real app, you'd generate this list programmatically or from a schema.

    # RFM features
    Recency: float = Field(..., description="Days since customer's last transaction.")
    Frequency: float = Field(..., description="Total number of transactions by customer.")
    Monetary: float = Field(..., description="Total monetary value of transactions by customer.")
    Monetary_log: float = Field(..., description="Log-transformed total monetary value.")

    # Aggregated numerical features (examples)
    TransactionAmount_mean: float = Field(..., description="Mean of transaction amounts.")
    Value_max: float = Field(..., description="Maximum transaction value.")
    TransactionHour_mean: float = Field(..., description="Mean hour of transactions.")
    IsWeekend_mean: float = Field(..., description="Proportion of weekend transactions.")

    # High-risk flags/counts (examples)
    ever_fraud: int = Field(..., description="Whether customer ever had a fraudulent transaction (0 or 1).")
    high_risk_product_category_count: int = Field(..., description="Count of transactions in high-risk product categories.")
    high_risk_pricing_strategy_count: int = Field(..., description="Count of transactions with high-risk pricing strategies.")
    high_risk_provider_count: int = Field(..., description="Count of transactions with high-risk providers.")

    # One-hot encoded features (examples - you'll have many of these)
    ProductCategory_airtime_sum: int = Field(..., description="Count of 'airtime' product category transactions.")
    ChannelId_ChannelId_3_sum: int = Field(..., description="Count of 'ChannelId_3' transactions.")
    ProviderId_ProviderId_3_sum: int = Field(..., description="Count of 'ProviderId_3' transactions.")
    ProductId_Grouped_Other_Product_sum: int = Field(..., description="Count of 'Other Product' transactions.")

    # Add all other 69 features here as per your final_customer_df.columns
    # For a full list, you'd ideally load your final_customer_df and iterate its columns
    # For now, this subset demonstrates the concept.

    class Config:
        # Example data for FastAPI's auto-generated documentation (Swagger UI)
        schema_extra = {
            "example": {
                "Recency": 10.0,
                "Frequency": 5.0,
                "Monetary": 5000.0,
                "Monetary_log": 8.5,
                "TransactionAmount_mean": 1000.0,
                "Value_max": 2000.0,
                "TransactionHour_mean": 14.5,
                "IsWeekend_mean": 0.2,
                "ever_fraud": 0,
                "high_risk_product_category_count": 0,
                "high_risk_pricing_strategy_count": 0,
                "high_risk_provider_count": 0,
                "ProductCategory_airtime_sum": 2,
                "ChannelId_ChannelId_3_sum": 3,
                "ProviderId_ProviderId_3_sum": 0,
                "ProductId_Grouped_Other_Product_sum": 0
                # ... add example values for all 69 features
            }
        }

# Define the output schema for the /predict endpoint
class PredictionResponse(BaseModel):
    customer_id: str = Field(..., description="The ID of the customer for whom the prediction was made.")
    risk_probability: float = Field(..., ge=0.0, le=1.0, description="Predicted probability of being a high-risk customer (0.0 to 1.0).")
    risk_label: int = Field(..., description="Predicted risk label (0 for Low Risk, 1 for High Risk).")
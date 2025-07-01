# src/data_processing.py

import pandas as pd
import numpy as np
import datetime as dt

def calculate_rfm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates Recency, Frequency, and Monetary (RFM) features for each customer.

    Args:
        df (pd.DataFrame): The input DataFrame containing transaction data
                           with 'CustomerId', 'TransactionStartTime', and 'Value' columns.

    Returns:
        pd.DataFrame: A DataFrame with 'CustomerId' and calculated 'Recency',
                      'Frequency', 'Monetary', and 'Monetary_log' features.
    """
    if not all(col in df.columns for col in ['CustomerId', 'TransactionStartTime', 'Value']):
        raise ValueError("Input DataFrame must contain 'CustomerId', 'TransactionStartTime', and 'Value' columns.")

    # Ensure TransactionStartTime is datetime
    if not pd.api.types.is_datetime64_any_dtype(df['TransactionStartTime']):
        df['TransactionStartTime'] = pd.to_datetime(df['TransactionStartTime'])

    # Determine the analysis date (one day after the last transaction)
    snapshot_date = df['TransactionStartTime'].max() + dt.timedelta(days=1)

    # Group by CustomerId to calculate RFM
    customer_df = df.groupby('CustomerId').agg(
        Recency=('TransactionStartTime', lambda date: (snapshot_date - date.max()).days),
        Frequency=('TransactionId', 'nunique'), # Use TransactionId for unique transaction count
        Monetary=('Value', 'sum') # Sum of absolute transaction values
    ).reset_index()

    # Apply log transformation to Monetary value
    customer_df['Monetary_log'] = np.log1p(customer_df['Monetary'])

    return customer_df

# You can add other helper functions here as we progress, e.g., for proxy creation, encoding
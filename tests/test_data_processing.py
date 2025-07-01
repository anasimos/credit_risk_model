# tests/test_data_processing.py

import pandas as pd
import numpy as np
import pytest
from src.data_processing import calculate_rfm # Import the function we want to test

# Test Case 1: Basic functionality with valid data
def test_calculate_rfm_basic_functionality():
    """
    Test that calculate_rfm correctly computes RFM for a simple, valid dataset.
    """
    # Create a sample DataFrame for testing
    data = {
        'CustomerId': ['C1', 'C1', 'C2', 'C2', 'C1', 'C3'],
        'TransactionId': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'],
        'TransactionStartTime': [
            '2023-01-01 10:00:00',
            '2023-01-05 12:00:00',
            '2023-01-02 09:00:00',
            '2023-01-06 11:00:00',
            '2023-01-10 15:00:00', # Latest for C1
            '2023-01-03 14:00:00'
        ],
        'Value': [100, 200, 50, 150, 300, 1000]
    }
    df_test = pd.DataFrame(data)

    # Expected results (calculated manually for this small dataset)
    # Snapshot date will be 2023-01-11 (day after 2023-01-10)
    # C1: Last transaction 2023-01-10 -> Recency = (2023-01-11 - 2023-01-10) = 1 day
    #     Frequency = 3 unique transactions
    #     Monetary = 100 + 200 + 300 = 600
    # C2: Last transaction 2023-01-06 -> Recency = (2023-01-11 - 2023-01-06) = 5 days
    #     Frequency = 2 unique transactions
    #     Monetary = 50 + 150 = 200
    # C3: Last transaction 2023-01-03 -> Recency = (2023-01-11 - 2023-01-03) = 8 days
    #     Frequency = 1 unique transaction
    #     Monetary = 1000

    expected_data = {
        'CustomerId': ['C1', 'C2', 'C3'],
        'Recency': [1, 5, 8],
        'Frequency': [3, 2, 1],
        'Monetary': [600, 200, 1000]
    }
    expected_df = pd.DataFrame(expected_data)
    expected_df['Monetary_log'] = np.log1p(expected_df['Monetary']) # Calculate log for expected

    # Call the function
    result_df = calculate_rfm(df_test.copy())

    # Sort both DataFrames by CustomerId to ensure consistent comparison
    result_df = result_df.sort_values(by='CustomerId').reset_index(drop=True)
    expected_df = expected_df.sort_values(by='CustomerId').reset_index(drop=True)

    # Assertions
    pd.testing.assert_frame_equal(result_df, expected_df, check_dtype=True, check_exact=False, rtol=1e-3)
    # check_exact=False and rtol for float comparisons

# Test Case 2: Handling missing required columns (error handling)
def test_calculate_rfm_missing_columns():
    """
    Test that calculate_rfm raises a ValueError if required columns are missing.
    """
    # Create a DataFrame missing 'Value' column
    data_missing_value = {
        'CustomerId': ['C1', 'C2'],
        'TransactionId': ['T1', 'T2'],
        'TransactionStartTime': ['2023-01-01', '2023-01-02']
    }
    df_missing_value = pd.DataFrame(data_missing_value)

    # Assert that a ValueError is raised
    with pytest.raises(ValueError, match="Input DataFrame must contain 'CustomerId', 'TransactionStartTime', and 'Value' columns."):
        calculate_rfm(df_missing_value)

    # Create a DataFrame missing 'CustomerId' column
    data_missing_customerid = {
        'TransactionId': ['T1', 'T2'],
        'TransactionStartTime': ['2023-01-01', '2023-01-02'],
        'Value': [100, 200]
    }
    df_missing_customerid = pd.DataFrame(data_missing_customerid)

    with pytest.raises(ValueError, match="Input DataFrame must contain 'CustomerId', 'TransactionStartTime', and 'Value' columns."):
        calculate_rfm(df_missing_customerid)

# Test Case 3 (Optional but good practice): Empty DataFrame input
def test_calculate_rfm_empty_dataframe():
    """
    Test that calculate_rfm handles an empty DataFrame gracefully.
    """
    df_empty = pd.DataFrame(columns=['CustomerId', 'TransactionId', 'TransactionStartTime', 'Value'])
    result_df = calculate_rfm(df_empty)

    assert result_df.empty
    assert 'Recency' in result_df.columns
    assert 'Frequency' in result_df.columns
    assert 'Monetary' in result_df.columns
    assert 'Monetary_log' in result_df.columns
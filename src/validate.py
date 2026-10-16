
import pandas as pd


def validate_data(df):
    print("Validating dataset...")

    # Check 1: Required columns
    required_columns = (
        ["Time", "Amount", "Class"]
        + [f"V{i}" for i in range(1, 29)]
    )

    missing_columns = [
        col for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Check 2: Missing values
    if df[required_columns].isnull().any().any():
        raise ValueError("Dataset contains missing values")

    # Check 3: Valid target labels
    valid_labels = {0, 1}

    if not set(df["Class"].unique()).issubset(valid_labels):
        raise ValueError(
            "Class column must contain only 0 and 1"
        )

    # Check 4: Numeric data
    if not all(
        pd.api.types.is_numeric_dtype(df[col])
        for col in required_columns
    ):
        raise ValueError(
            "Required columns must contain numeric data"
        )

    print("Data validation passed!")
    return True

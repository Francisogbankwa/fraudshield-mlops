import pandas as pd
import pytest

from src.validate import validate_data


@pytest.fixture
def valid_data():
    columns = {
        "Time": [1.0, 2.0],
        "Amount": [100.0, 200.0],
        "Class": [0, 1],
    }

    for i in range(1, 29):
        columns[f"V{i}"] = [0.1, 0.2]

    return pd.DataFrame(columns)


def test_valid_data_passes(valid_data):
    assert validate_data(valid_data) is True


def test_missing_column_fails(valid_data):
    bad_data = valid_data.drop(columns=["Amount"])

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_data(bad_data)


def test_missing_values_fail(valid_data):
    bad_data = valid_data.copy()
    bad_data.loc[0, "Amount"] = None

    with pytest.raises(ValueError, match="missing values"):
        validate_data(bad_data)


def test_invalid_labels_fail(valid_data):
    bad_data = valid_data.copy()
    bad_data.loc[0, "Class"] = 5

    with pytest.raises(ValueError, match="only 0 and 1"):
        validate_data(bad_data)


def test_non_numeric_data_fails(valid_data):
    bad_data = valid_data.copy()
    bad_data["Amount"] = ["invalid", "100"]

    with pytest.raises(ValueError, match="numeric data"):
        validate_data(bad_data)

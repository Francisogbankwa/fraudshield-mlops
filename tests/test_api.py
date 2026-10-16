from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@patch("src.api.load_threshold")
@patch("src.api.load_model")
def test_predict_endpoint(mock_load_model, mock_load_threshold):
    fake_model = MagicMock()
    fake_model.predict_proba.return_value = [[0.2, 0.8]]

    mock_load_model.return_value = fake_model
    mock_load_threshold.return_value = 0.7

    transaction = {
        "Time": 1000,
        "Amount": 50,
        "features": [0.0] * 28,
    }

    response = client.post("/predict", json=transaction)

    assert response.status_code == 200

    result = response.json()

    assert result["fraud_probability"] == 0.8
    assert result["fraud_prediction"] == 1
    assert result["threshold"] == 0.7

    fake_model.predict_proba.assert_called_once()


def test_invalid_transaction():
    transaction = {
        "Time": 1000,
        "Amount": -50,
        "features": [0.0] * 28,
    }

    response = client.post("/predict", json=transaction)

    assert response.status_code == 422
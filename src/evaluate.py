from sklearn.metrics import (
    average_precision_score,
    precision_score,
    recall_score,
    f1_score,
)


def evaluate_model(model, X, y, threshold=0.5):
    probabilities = model.predict_proba(X)[:, 1]
    predictions = (probabilities >= threshold).astype(int)

    metrics = {
        "average_precision": float(
            average_precision_score(y, probabilities)
        ),
        "precision": float(
            precision_score(y, predictions, zero_division=0)
        ),
        "recall": float(
            recall_score(y, predictions, zero_division=0)
        ),
        "f1": float(
            f1_score(y, predictions, zero_division=0)
        ),
    }

    return metrics

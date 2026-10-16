
from pathlib import Path
import json
import joblib
import mlflow
import mlflow.sklearn

from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from data import load_data, split_data
from evaluate import evaluate_model


ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"


def main():
    # STEP 1: Load and split data
    df = load_data()

    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)

    print("Training samples:", len(X_train))
    print("Validation samples:", len(X_val))
    print("Test samples:", len(X_test))

    # STEP 2: Create model
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(
            class_weight="balanced",
            max_iter=1000,
            random_state=42,
        ),
    )

    # STEP 3: Configure MLflow
    mlflow.set_tracking_uri(
        f"sqlite:///{(ROOT / 'mlflow.db').as_posix()}"
    )
    mlflow.set_experiment("FraudShield-Experiments")

    with mlflow.start_run(run_name="modular-training-pipeline"):
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("class_weight", "balanced")
        mlflow.log_param("max_iter", 1000)
        mlflow.log_param("split", "chronological-60-20-20")

        # STEP 4: Train on training data only
        model.fit(X_train, y_train)

        # STEP 5: Choose threshold using validation data
        best_threshold = 0.5
        best_f1 = -1.0

        for threshold in [0.5, 0.7, 0.9, 0.95, 0.99]:
            val_metrics = evaluate_model(
                model, X_val, y_val, threshold
            )

            print(
                f"Threshold {threshold:.2f} | "
                f"Validation F1: {val_metrics['f1']:.3f}"
            )

            if val_metrics["f1"] > best_f1:
                best_f1 = val_metrics["f1"]
                best_threshold = threshold

        print("Selected threshold:", best_threshold)

        # STEP 6: Final evaluation on untouched test data
        metrics = evaluate_model(
            model, X_test, y_test, best_threshold
        )

        print("Final test metrics:")
        print(json.dumps(metrics, indent=2))

        # STEP 7: Save results
        MODEL_DIR.mkdir(exist_ok=True)

        joblib.dump(model, MODEL_DIR / "fraud_model.joblib")

        with open(MODEL_DIR / "metrics.json", "w") as file:
            json.dump(metrics, file, indent=2)

        with open(MODEL_DIR / "threshold.json", "w") as file:
            json.dump({"threshold": best_threshold}, file, indent=2)

        # STEP 8: Track everything in MLflow
        mlflow.log_param("selected_threshold", best_threshold)
        mlflow.log_metric("validation_best_f1", best_f1)
        mlflow.log_metrics(metrics)

        mlflow.sklearn.log_model(model, name="fraud-model")
        mlflow.log_artifact(str(MODEL_DIR / "metrics.json"))
        mlflow.log_artifact(str(MODEL_DIR / "threshold.json"))

        print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()

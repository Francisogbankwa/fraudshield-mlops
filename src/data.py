from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "creditcard.csv"


def load_data():
    df = pd.read_csv(DATA_PATH)

    print("Dataset shape:", df.shape)
    print("Fraud rate:", f"{df['Class'].mean():.4%}")

    return df


def split_data(df):
    # Sort transactions chronologically
    df = df.sort_values("Time").reset_index(drop=True)

    X = df.drop(columns=["Class"])
    y = df["Class"]

    # 60% training, 20% validation, 20% testing
    train_end = int(len(df) * 0.6)
    val_end = int(len(df) * 0.8)

    X_train = X.iloc[:train_end]
    y_train = y.iloc[:train_end]

    X_val = X.iloc[train_end:val_end]
    y_val = y.iloc[train_end:val_end]

    X_test = X.iloc[val_end:]
    y_test = y.iloc[val_end:]

    return X_train, X_val, X_test, y_train, y_val, y_test
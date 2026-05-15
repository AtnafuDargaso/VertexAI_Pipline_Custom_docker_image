import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, required=True, help="Path to input dataset (CSV)")
    parser.add_argument("--model_dir", type=str, required=True, help="Path to save the trained model")
    parser.add_argument("--metrics_path", type=str, required=True, help="Path to save metrics")
    args = parser.parse_args()

    print(f"Loading data from {args.data_path}")
    # In a real scenario, this would load actual data. Creating dummy data for demonstration.
    if args.data_path == "dummy_data":
        from sklearn.datasets import make_classification
        X, y = make_classification(n_samples=1000, n_features=20, random_state=42)
        df = pd.DataFrame(X)
        df['target'] = y
    else:
        df = pd.read_csv(args.data_path)

    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training RandomForest model for churn prediction...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"Model Accuracy: {acc}")

    # Save model
    os.makedirs(args.model_dir, exist_ok=True)
    model_path = os.path.join(args.model_dir, "model.joblib")
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    # Save metrics
    os.makedirs(os.path.dirname(args.metrics_path), exist_ok=True)
    with open(args.metrics_path, "w") as f:
        f.write(f"{acc}")
    print(f"Metrics saved to {args.metrics_path}")

if __name__ == "__main__":
    main()

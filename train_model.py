from pathlib import Path
import json
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import OneHotEncoder
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
MODELS = ROOT / "models"
EVIDENCE = ROOT / "evidence"
MODELS.mkdir(exist_ok=True)
EVIDENCE.mkdir(exist_ok=True)

RENAME = {
    "Installations": "Installs & Demo",
    "Consumables": "Filters & Consumables",
}

def canonical_team(value):
    return RENAME.get(str(value).strip(), str(value).strip())

def build_pipeline():
    text_features = FeatureUnion([
        ("word", TfidfVectorizer(
            ngram_range=(1, 2), min_df=2, sublinear_tf=True,
            max_features=60000
        )),
        ("char", TfidfVectorizer(
            analyzer="char_wb", ngram_range=(3, 5), min_df=3,
            sublinear_tf=True, max_features=60000
        )),
    ])
    preprocess = ColumnTransformer([
        ("text", text_features, "request_text"),
        ("cat", OneHotEncoder(handle_unknown="ignore"),
         ["channel", "product_family", "warranty_status", "source"]),
    ])
    return Pipeline([
        ("pre", preprocess),
        ("clf", LinearSVC(C=1.0)),
    ])

def main():
    source_dir = DATA
    if not (source_dir / "Train.csv").exists() and (DATA / "assignment files" / "Train.csv").exists():
        source_dir = DATA / "assignment files"
    train_path = source_dir / "Train.csv"
    if not train_path.exists():
        raise FileNotFoundError(
            f"Missing Train.csv. Extract the supplied assignment ZIP into data/; "
            f"the script checks both data/ and data/assignment files/."
        )

    df = pd.read_csv(train_path)
    required = {
        "request_id", "created_at_ist", "channel", "product_family",
        "warranty_status", "request_text", "source", "team_label"
    }
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Train.csv is missing columns: {sorted(missing)}")

    df["created_at_ist"] = pd.to_datetime(df["created_at_ist"], errors="coerce")
    df["team"] = df["team_label"].map(canonical_team)
    if df["team"].isna().any():
        raise ValueError("Some training rows have no team label.")

    # Time-based validation: train on records before 1 Apr 2026,
    # validate on Apr-Jun 2026. This mirrors the CRM-only future test period.
    cutoff = pd.Timestamp("2026-04-01")
    fit_df = df[df["created_at_ist"] < cutoff].copy()
    valid_df = df[df["created_at_ist"] >= cutoff].copy()
    if fit_df.empty or valid_df.empty:
        raise ValueError("Time split produced an empty train or validation set.")

    model = build_pipeline()
    model.fit(fit_df, fit_df["team"])
    valid_pred = model.predict(valid_df)

    acc = accuracy_score(valid_df["team"], valid_pred)
    macro_f1 = f1_score(valid_df["team"], valid_pred, average="macro")
    report = classification_report(
        valid_df["team"], valid_pred, output_dict=True, zero_division=0
    )
    labels = sorted(df["team"].unique())
    cm = confusion_matrix(valid_df["team"], valid_pred, labels=labels)
    pd.DataFrame(cm, index=labels, columns=labels).to_csv(
        EVIDENCE / "confusion_matrix.csv"
    )
    pd.DataFrame({
        "request_id": valid_df["request_id"].values,
        "actual_team": valid_df["team"].values,
        "predicted_team": valid_pred,
    }).to_csv(EVIDENCE / "validation_predictions.csv", index=False)

    metrics = {
        "validation_method": "Chronological holdout",
        "train_period_end_exclusive": "2026-04-01",
        "validation_period": "2026-04-01 through 2026-06-30",
        "train_rows": int(len(fit_df)),
        "validation_rows": int(len(valid_df)),
        "accuracy": float(acc),
        "macro_f1": float(macro_f1),
        "error_count": int((valid_df["team"].values != valid_pred).sum()),
        "error_rate": float(1 - acc),
        "classification_report": report,
    }
    (EVIDENCE / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )

    # Final model is trained on all labelled historical records.
    final_model = build_pipeline()
    final_model.fit(df, df["team"])
    joblib.dump(final_model, MODELS / "routing_model.joblib")

    # Predict the unlabelled file in its original row order.
    test_path = source_dir / "test_unlabelled.csv"
    if not test_path.exists():
        raise FileNotFoundError(
            f"Missing {test_path}. Extract the supplied assignment files into data/."
        )
    test = pd.read_csv(test_path)
    predictions = final_model.predict(test)
    submission = pd.DataFrame({
        "request_id": test["request_id"],
        "team": predictions,
    })
    submission.to_csv(ROOT / "predictions.csv", index=False)

    print(f"Validation rows: {len(valid_df)}")
    print(f"Accuracy: {acc:.4%}")
    print(f"Macro-F1: {macro_f1:.4f}")
    print(f"Validation errors: {metrics['error_count']}")
    print(f"Final predictions written: {len(submission)} rows")
    print("Model saved to models/routing_model.joblib")

if __name__ == "__main__":
    main()

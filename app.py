from pathlib import Path
import re
import joblib
import pandas as pd
from flask import Flask, jsonify, render_template, request


ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "models" / "routing_model.joblib"

TEAM_HANDLES = {
    "Installs & Demo": "New-product installation, demonstrations and wall-mounting visits.",
    "Repairs": "Product faults, breakdowns, error codes, noise and leaks that need a technician.",
    "Filters & Consumables": "Filters, candles, membranes, jars, brushes, blades and AMC kits; not product faults.",
    "Billing": "Payment problems such as invoices, GST, double charges, payment refunds and EMI conversion.",
    "Returns & Replacement": "Damaged, wrong or incomplete deliveries, returns and exchanges.",
    "Warranty Claims": "Warranty and Kestrel Shield registration, coverage questions and claim status.",
    "Product Advice": "Pre- and post-purchase usage questions when no fault is reported.",
}

REQUIRED = ["channel", "product_family", "warranty_status", "request_text", "source"]

app = Flask(__name__)
_model = None

def get_model():
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Model not found. Run `python train_model.py` before starting the app."
            )
        _model = joblib.load(MODEL_PATH)
    return _model

def explain_prediction(model, row, predicted_team):
    reasons = []
    text = str(row.get("request_text", "")).lower()

    # Explain using the strongest positive text-feature contributions
    # from the trained linear classifier. These are model signals, not policy rules.
    try:
        pre = model.named_steps["pre"]
        clf = model.named_steps["clf"]
        x = pre.transform(pd.DataFrame([row]))
        class_index = list(clf.classes_).index(predicted_team)
        contributions = x.multiply(clf.coef_[class_index]).tocoo()
        names = pre.get_feature_names_out()
        ranked = sorted(
            zip(contributions.col, contributions.data),
            key=lambda item: item[1], reverse=True
        )
        terms = []
        for idx, value in ranked:
            if value <= 0:
                break
            feature = str(names[idx])
            if not feature.startswith("text__"):
                continue
            term = feature.split("__")[-1].strip()
            if term and term not in terms and len(term) > 1:
                terms.append(term)
            if len(terms) == 3:
                break
        if terms:
            reasons.append(
                "Wording that supported this prediction: " + ", ".join(terms) + "."
            )
    except Exception:
        pass

    product = str(row.get("product_family", "")).strip()
    warranty = str(row.get("warranty_status", "")).strip().replace("_", " ")
    channel = str(row.get("channel", "")).strip()
    if product:
        reasons.append(f"Product recorded: {product}.")
    if warranty:
        reasons.append(f"Warranty status recorded: {warranty}.")
    if channel:
        reasons.append(f"Request received through: {channel}.")

    reasons.append("Team scope: " + TEAM_HANDLES.get(predicted_team, "See team directory."))
    reasons.append(
        "This is a model recommendation, not a confirmed diagnosis or warranty decision. "
        "Review ambiguous or multi-issue requests before transfer."
    )
    return reasons

@app.get("/")
def home():
    model_ready = MODEL_PATH.exists()
    return render_template("index.html", model_ready=model_ready)

@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_ready": MODEL_PATH.exists(),
        "service": "Kestrel Home Service Routing"
    })

@app.post("/api/predict")
def predict():
    try:
        model = get_model()
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 503

    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send one JSON object in the request body."}), 400

    missing = [key for key in REQUIRED if not str(payload.get(key, "")).strip()]
    if missing:
        return jsonify({"error": "Missing required fields: " + ", ".join(missing)}), 400

    row = {key: str(payload.get(key, "")).strip() for key in REQUIRED}
    # Keep the API input aligned with the model's training columns.
    frame = pd.DataFrame([row])
    predicted_team = str(model.predict(frame)[0])
    return jsonify({
        "request_id": payload.get("request_id"),
        "predicted_team": predicted_team,
        "team_scope": TEAM_HANDLES.get(predicted_team, ""),
        "reasons": explain_prediction(model, row, predicted_team),
        "note": "The reasons describe model signals and supplied record fields; they are not causal proof."
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

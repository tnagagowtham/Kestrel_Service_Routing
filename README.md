# Kestrel Home — Service Request Routing

A local, no-paid-API service-routing prototype. It predicts the initial queue label from the historical `team_label` field and returns employee-readable model signals.

## Important data-handling note

The Kestrel operations policy says customer and operational data must not be published or shared beyond the engagement team. Keep the original CSV/PDF/TXT files private. Do not commit the `data/` folder or trained model to a public repository. The required `predictions.csv` is included at the repository root.

## 1. Setup

Requires Python 3.10+.

1. Extract the original assignment ZIP into `data/`. The script accepts either files directly inside `data/` or inside the ZIP's `assignment files/` subfolder. Keep the original filenames, including capital `Train.csv`.
2. Create and activate a virtual environment:

### Windows PowerShell

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

### Windows Command Prompt

```bat
py -m venv .venv
.venv\Scripts\activate.bat
```

3. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## 2. Train, validate and generate predictions

```bash
python train_model.py
```

This:
- creates a chronological validation split (train before 1 Apr 2026; validate Apr–Jun 2026);
- reports accuracy, macro-F1, class-wise metrics and validation errors;
- saves a confusion matrix and validation predictions under `evidence/`;
- fits the final model on all labelled data;
- writes `models/routing_model.joblib`;
- regenerates `predictions.csv` in the required `request_id,team` format.

Old team names are normalized:
- `Installations` → `Installs & Demo`
- `Consumables` → `Filters & Consumables`

## 3. Start the service

```bash
python app.py
```

Open http://127.0.0.1:5000

The browser screen calls the JSON endpoint below. No paid API key or external model API is used.

## 4. API

`POST /api/predict`

Example:

```bash
curl -X POST http://127.0.0.1:5000/api/predict ^
  -H "Content-Type: application/json" ^
  -d "{\"channel\":\"chat\",\"product_family\":\"Water Purifier\",\"warranty_status\":\"in_warranty\",\"request_text\":\"Water purifier is leaking from the bottom and has stopped working\",\"source\":\"crm\"}"
```

Required JSON fields:
- `channel`
- `product_family`
- `warranty_status`
- `request_text`
- `source`

Returns `predicted_team`, team scope, and reasons based on influential wording plus the submitted record fields. These reasons describe model signals; they are not causal proof or a warranty decision.

Health check: `GET /health`.

## 5. Model and evaluation

The initial model is a TF-IDF word/character n-gram representation plus one-hot encoded request metadata, trained with a Linear Support Vector Classifier. The target is the historical `team_label` (the bot's initial queue), because the assignment asks for agreement with those labels. The `resolution_log.final_team` is analysed separately; it is not substituted as the training target.

Primary score: accuracy, because the brief explicitly sets a 90% label-match bar. Macro-F1 is also reported so smaller teams are not hidden by the largest class.

The supplied dataset spans 1 Apr 2025–30 Jun 2026 (15 calendar months by timestamps), despite the email describing eighteen months. The held-out validation period is Apr–Jun 2026 and is CRM-only, like the unlabelled Jul–Sep 2026 data.

## 6. Public GitHub checklist

Before publishing:
- Keep `data/` private and verify it is ignored by Git.
- Keep `models/routing_model.joblib` private unless the data owner explicitly approves publishing it.
- Include `predictions.csv`, code, README, memo and submission-form answers.
- Do not upload the original customer/operations data.

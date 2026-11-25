
import pandas as pd
from pathlib import Path

# Project directory
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

# Automatically locate the test dataset
test_files = list(DATA_DIR.rglob("test_unlabelled.csv"))

if not test_files:
    raise FileNotFoundError(
        "test_unlabelled.csv not found. Check your data folder."
    )

# Load files
test = pd.read_csv(test_files[0])
predictions = pd.read_csv(ROOT / "predictions.csv")

# Combine request dates and predictions
data = test.merge(predictions, on="request_id")

# Convert timestamps
data["created_at_ist"] = pd.to_datetime(data["created_at_ist"])

# Extract month
data["month"] = data["created_at_ist"].dt.to_period("M").astype(str)

# Calculate monthly workload
monthly = pd.crosstab(data["month"], data["team"])

print("\nMONTHLY TEAM WORKLOAD\n")
print(monthly.to_string())

# Save output
output_dir = ROOT / "evidence"
output_dir.mkdir(exist_ok=True)

monthly.to_csv(output_dir / "monthly_team_workload.csv")

print("\nAnalysis completed successfully!")
print("Saved: evidence/monthly_team_workload.csv")

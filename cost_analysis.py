
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"

# Locate resolution log
files = list(DATA_DIR.rglob("resolution_log.csv"))

if not files:
    raise FileNotFoundError("resolution_log.csv not found in data folder.")

df = pd.read_csv(files[0])

# Calculate historical routing costs
transfer_cost = 305
contact_cost = 260

total_transfers = df["transfers"].sum()
misrouted_requests = (df["transfers"] > 0).sum()

total_transfer_cost = total_transfers * transfer_cost
total_contact_cost = misrouted_requests * contact_cost
total_cost = total_transfer_cost + total_contact_cost

annual_bot_cost = 320000

print("\nHISTORICAL ROUTING COST ANALYSIS")
print("-" * 40)
print("Total requests:", len(df))
print("Requests with transfers:", misrouted_requests)
print("Total transfers:", total_transfers)
print("Transfer cost: ₹", total_transfer_cost)
print("Extra contact cost: ₹", total_contact_cost)
print("Combined historical cost: ₹", total_cost)
print("Annual bot licence: ₹", annual_bot_cost)

# Save report
report = pd.DataFrame({
    "Metric": [
        "Total requests",
        "Requests with transfers",
        "Total transfers",
        "Transfer cost",
        "Extra contact cost",
        "Combined historical cost",
        "Annual bot licence"
    ],
    "Value": [
        len(df),
        misrouted_requests,
        total_transfers,
        total_transfer_cost,
        total_contact_cost,
        total_cost,
        annual_bot_cost
    ]
})

report.to_csv(ROOT / "evidence" / "cost_analysis.csv", index=False)

print("\nSaved: evidence/cost_analysis.csv")

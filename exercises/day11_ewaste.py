from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import pandas as pd
ew = pd.read_csv((ROOT / "data/raw/bank_ewaste.csv"))
ew["total_ewaste_kg"] = ew["desktops_kg"] + ew["atm_terminals_kg"] + ew["laptops_kg"]
ew["recycling_ratio"] = (ew["recycled_kg"] / ew["total_ewaste_kg"] * 100).round(1)
print(ew[["bank", "quarter", "total_ewaste_kg", "recycling_ratio"]])
print(ew.shape)
ew.to_csv((ROOT / "data/processed/bank_ewaste_metrics.csv"), index=False)


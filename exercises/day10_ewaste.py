from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import pandas as pd
ew = pd.read_csv((ROOT / "data/raw/bank_ewaste.csv"))
print(ew.shape)
print(ew.head())

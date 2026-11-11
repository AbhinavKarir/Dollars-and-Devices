from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import pandas as pd
df = pd.read_csv((ROOT / "data/raw/bank_financials.csv"))
print(df.head())
print(df.shape)
print(df.info())
print(df.describe())

df["efficiency_ratio"] = (df["expenses"]/df["revenue"] * 100)
q2 = df[df["quarter"] == "2026-Q2"]
print(q2[["bank", "efficiency_ratio"]].round(1))

avg_efficiency = df.groupby("bank")["efficiency_ratio"].mean().round(1)
print(avg_efficiency)

df.to_csv((ROOT / "data/processed/bank_metrics.csv"), index=False)

#Exercise for me
print(df.columns)
df["net_margin"] = (df["net_income"]/df["revenue"] * 100).round(1)
print(df[["bank", "net_margin", "quarter"]].sort_values("net_margin", ascending=False).head(1))
avg_net_margin = df.groupby("bank")["net_margin"].mean().round(1)
print(avg_net_margin)
to_csv = (df.to_csv((ROOT / "data/processed/bank_metrics.csv"), index=False))


import pandas as pd
#Simulated Figures in C$ millions
data = {
    "bank": ["Alder Bank", "Birch Trust", "Juniper Bank", "Maple Harbour Bank", "Cedar Bank", "Spruce Financial"],
    "revenue": [15000, 14000, 9000, 9500, 7500, 3500],
    "expenses": [7900, 6500, 5500, 4500, 5000, 6000],
}
df = pd.DataFrame(data)
print(df)

print(df.shape)
print(df.columns)
print(df.head(3))

print(df["bank"])
print(df["revenue"].sum())
print(df["revenue"].mean())

df["efficiency_ratio"] = (df["expenses"]/df["revenue"] * 100).round(1)
print(df)

strong = df[df["efficiency_ratio"] < 55]
print(strong)

ranked = df.sort_values("efficiency_ratio")
print(ranked)

print(df.columns)
df["earnings_gap"] = df["revenue"] - df["expenses"]
print(df)

df.sort_values("earnings_gap", ascending=False)
print("Earnings gap is above 9000") if df["earnings_gap"].max() > 9000 else print("Earnings gap is below 9000")


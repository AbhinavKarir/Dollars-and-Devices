import pandas as pd
import plotly.express as px
df = pd.read_csv("data/processed/bank_metrics.csv")
print(df.head())

avg_efficiency = df.groupby("bank")["efficiency_ratio"].mean().round(1).reset_index() #1
print(avg_efficiency)
fig = px.bar(avg_efficiency, x="bank", y="efficiency_ratio", title="Average Efficiency Ratio by Bank")
fig.show()

fig.update_layout(xaxis_title="Bank", yaxis_title="Average Efficieny Ratio (%)") #2

fig_bar = px.bar(df, x="bank", y="efficiency_ratio", text_auto=".1f", title="Efficiency Ratio by Bank and Quarter") #3
fig_bar.update_layout(xaxis_title = "Bank", yaxis_title = "Efficiency Ratio (%)")
fig_bar.show()

fig_line = px.line(df , x= "quarter", y = "efficiency_ratio", color = "bank", markers=True, title= "Efficiency Ratio by Bank Over Time(Lower is Better)")

fig_line.update_layout(xaxis_title= "Quarter", yaxis_title= "Efficiency_Ratio (%)")
fig_line.show()

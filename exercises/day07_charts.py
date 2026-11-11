from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import pandas as pd
import plotly.express as px
df = pd.read_csv((ROOT / "data/processed/bank_metrics.csv"))
print(df.columns) 

def make_line_chart(data, column, title, y_label):
    fig = px.line(data, x="quarter", y=column, color="bank", markers=True, title=title)
    fig.update_layout(yaxis_title=y_label)
    return fig
   

fig1= make_line_chart(df, "efficiency_ratio", "Efficiency Ratio by Bank Over Time(Lower is Better)", "Efficiency_Ratio (%)")
fig2 = make_line_chart(df, "net_margin", "Net Margin by Bank Over Time (Higher is Better)", "Net Margin (%)")
fig1.show()
fig2.show()

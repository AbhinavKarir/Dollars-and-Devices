from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(page_title="Canadian Bank Dashboard Overview", page_icon="🏦", layout="wide")
st.title ("Canadian Bank Dashboard (sample data) - By Abhinav Karir")
st.caption("Sample data for demonstration purposes only. Not for investment decisions.")
st.write("Compare how Canada's six largest banks stack up on cost efficiency and profitability. Pick a bank below to see its own trend.")
def percent_change(old,new):
    number_changed = new - old
    percent_change = (number_changed / old) * 100
    return percent_change
df = pd.read_csv((ROOT / "data/processed/bank_metrics.csv"))
bank = st.selectbox("Choose a Bank", df["bank"].unique())
bank_df = df[df["bank"] == bank]
st.dataframe(bank_df)

def make_line_chart(data, column, title, y_label):
    fig = px.line(data, x="quarter", y=column, color="bank", markers=True, title=title)
    fig.update_layout(yaxis_title= y_label , xaxis_title = "Quarter", legend_title = "Bank")
    return fig
   

fig1= make_line_chart(df, "efficiency_ratio", "Efficiency Ratio by Bank Over Time (Lower is Better)", "Efficiency Ratio (%)")
fig2 = make_line_chart(df, "net_margin", "Net Margin by Bank Over Time (Higher is Better)", "Net Margin (%)")
st.plotly_chart(fig1)
st.plotly_chart(fig2)

st.subheader(f"{bank} on its own")
fig3 = make_line_chart (bank_df, "efficiency_ratio", f"{bank} Efficiency Ratio Over Time (Lower is Better)", "Efficiency Ratio (%)")
st.plotly_chart(fig3)

st.dataframe(df)
bank_df = bank_df.sort_values("quarter")
first = bank_df.iloc[0]
latest = bank_df.iloc[-1]
eff_change = percent_change(first["efficiency_ratio"], latest["efficiency_ratio"])
margin_change = percent_change(first["net_margin"], latest["net_margin"])
st.write(df.shape)

col1 , col2 = st.columns(2)
with col1:
    st.metric("Efficiency Ratio (%)", f"{latest['efficiency_ratio']:.1f}", f"{eff_change:.1f}%", delta_color="inverse")
with col2:
    st.metric("Net Margin (%)", f"{latest['net_margin']:.1f}", f"{margin_change:.1f}%")

















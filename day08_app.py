import streamlit as st
import pandas as pd
import plotly.express as px
st.title ("Canadian Bank Dashboard (sample data) - By Abhinav Karir")
st.write("Compare how Canada's six largest banks stack up on cost efficiency and profitability. Pick a bank below to see its own trend.")

df = pd.read_csv("data/processed/bank_metrics.csv")
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

st.subheader(f"{bank} on it's own")
fig3 = make_line_chart (bank_df, "efficiency_ratio", f"{bank} Efficiency Ratio Over Time (Lower is Better)", "Efficiency Ratio (%)")
st.plotly_chart(fig3)

st.dataframe(df)
st.write(df.shape)















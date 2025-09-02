import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Weekly Excel Dashboard", layout="wide")

st.sidebar.header("Upload weekly Excel")
file = st.sidebar.file_uploader("Choose .xlsx", type=["xlsx"])

REQUIRED = ["Week","Category","Region","Revenue","Transactions"]

if file:
    df = pd.read_excel(file, engine="openpyxl")
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        st.error(f"Missing columns: {missing}")
        st.stop()

    df["Week"] = pd.to_datetime(df["Week"], errors="coerce")
    for c in ["Revenue","Transactions"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    st.sidebar.subheader("Filters")
    category = st.sidebar.selectbox("Category", ["All"]+sorted(df["Category"].dropna().unique().tolist()))
    region = st.sidebar.selectbox("Region", ["All"]+sorted(df["Region"].dropna().unique().tolist()))

    f = df.copy()
    if category!="All": f = f[f["Category"]==category]
    if region!="All":   f = f[f["Region"]==region]

    c1,c2,c3 = st.columns(3)
    c1.metric("Total Revenue", f'{f["Revenue"].sum():,.0f}')
    c2.metric("Transactions", f'{f["Transactions"].sum():,.0f}')
    c3.metric("Avg Rev/Txn", f'{(f["Revenue"].sum()/max(f["Transactions"].sum(),1)):,.2f}')

    st.subheader("Revenue Over Time")
    st.plotly_chart(
        px.line(f.groupby("Week",as_index=False)["Revenue"].sum(), x="Week", y="Revenue", markers=True),
        use_container_width=True
    )

    st.subheader("By Category")
    st.plotly_chart(
        px.bar(f.groupby("Category",as_index=False)["Revenue"].sum().sort_values("Revenue",ascending=False),
               x="Category", y="Revenue", text_auto=True),
        use_container_width=True
    )

    st.subheader("Rows")
    st.dataframe(f)
else:
    st.info("Upload this week’s Excel with columns: " + ", ".join(REQUIRED))

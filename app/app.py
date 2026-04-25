import streamlit as st
import pandas as pd
import os
import plotly.express as px

# =========================
# LOAD DATA
# =========================
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "recalls_raw.csv")
df = pd.read_csv(file_path)

df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
df['Year'] = df['Date'].dt.year

# =========================
# TITLE
# =========================
st.title("📊 FDA Recall Intelligence Dashboard")

# =========================
# SIDEBAR FILTERS
# =========================
company = st.sidebar.selectbox("Company", ["All"] + sorted(df["Company"].dropna().unique().tolist()))
product_type = st.sidebar.selectbox("Product Type", ["All"] + sorted(df["ProductType"].dropna().unique().tolist()))

# =========================
# FILTER DATA
# =========================
filtered_df = df.copy()

if company != "All":
    filtered_df = filtered_df[filtered_df["Company"] == company]

if product_type != "All":
    filtered_df = filtered_df[filtered_df["ProductType"] == product_type]

# =========================
# KPI CARDS
# =========================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Recalls", len(filtered_df))
col2.metric("Companies", filtered_df["Company"].nunique())
col3.metric("Product Types", filtered_df["ProductType"].nunique())

# =========================
# CHART 1: TOP COMPANIES
# =========================
st.subheader("🏢 Top Companies by Recalls")

top_companies = filtered_df["Company"].value_counts().head(10).reset_index()
top_companies.columns = ["Company", "Count"]

fig1 = px.bar(top_companies, x="Company", y="Count")
st.plotly_chart(fig1, use_container_width=True)

# =========================
# CHART 2: PRODUCT TYPE DISTRIBUTION
# =========================
st.subheader("📦 Product Type Distribution")

product_dist = filtered_df["ProductType"].value_counts().reset_index()
product_dist.columns = ["ProductType", "Count"]

fig2 = px.pie(product_dist, names="ProductType", values="Count")
st.plotly_chart(fig2, use_container_width=True)

# =========================
# CHART 3: TREND OVER TIME
# =========================
st.subheader("📈 Recall Trend Over Time")

trend = filtered_df.groupby("Year").size().reset_index(name="Count")

fig3 = px.line(trend, x="Year", y="Count")
st.plotly_chart(fig3, use_container_width=True)

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Data Preview")
st.dataframe(filtered_df.head(10))
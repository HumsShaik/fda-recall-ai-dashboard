import streamlit as st
import pandas as pd
import os
import plotly.express as px

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="FDA Recall Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================
# LOAD DATA
# =========================
file_path = os.path.join(os.path.dirname(__file__), "..", "data", "recalls_raw.csv")
df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df["Year"] = df["Date"].dt.year

# =========================
# SIDEBAR
# =========================
st.sidebar.title("🏥 FDA Recall AI")
st.sidebar.markdown("Healthcare + AI Analytics Platform")

company = st.sidebar.selectbox(
    "Company",
    ["All"] + sorted(df["Company"].dropna().unique().tolist())
)

product_type = st.sidebar.selectbox(
    "Product Type",
    ["All"] + sorted(df["ProductType"].dropna().unique().tolist())
)

# =========================
# TITLE
# =========================
st.markdown("""
### AI-Powered Healthcare Recall Intelligence

Analyze FDA recall trends, identify high-risk products, and explore recall insights using interactive analytics and semantic search.
""")

# =========================
# FILTER DATA
# =========================
filtered_df = df.copy()

if company != "All":
    filtered_df = filtered_df[filtered_df["Company"] == company]

if product_type != "All":
    filtered_df = filtered_df[filtered_df["ProductType"] == product_type]

search = st.text_input("🔍 Search Product or Company")

if search:
    filtered_df = filtered_df[
        filtered_df["ProductDescription"].str.contains(search, case=False, na=False) |
        filtered_df["Company"].str.contains(search, case=False, na=False)
    ]

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

# =========================
# EXECUTIVE INSIGHTS
# =========================
st.subheader("📌 Executive Insights")

top_company = filtered_df["Company"].value_counts().idxmax()
top_product = filtered_df["ProductType"].value_counts().idxmax()

st.info(f"""
- Highest recall frequency company: **{top_company}**
- Most affected product category: **{top_product}**
- Total recalls analyzed: **{len(filtered_df)}**
""")

# =========================
# KPI CARDS
# =========================
st.subheader("📌 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Recalls", len(filtered_df))
col2.metric("Companies", filtered_df["Company"].nunique())
col3.metric("Product Types", filtered_df["ProductType"].nunique())

# =========================
# CHART 1
# =========================
st.subheader("🏢 Top Companies by Recalls")

top_companies = filtered_df["Company"].value_counts().head(10).reset_index()
top_companies.columns = ["Company", "Count"]

fig1 = px.bar(
    top_companies,
    x="Company",
    y="Count",
    title="Top 10 Companies by Recall Count"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# CHART 2
# =========================
st.subheader("📦 Product Type Distribution")

product_dist = filtered_df["ProductType"].value_counts().reset_index()
product_dist.columns = ["ProductType", "Count"]

fig2 = px.pie(
    product_dist,
    names="ProductType",
    values="Count",
    title="Recall Distribution by Product Type"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# CHART 3
# =========================
st.subheader("📈 Recall Trend Over Time")

trend = filtered_df.groupby("Year").size().reset_index(name="Count")

fig3 = px.line(
    trend,
    x="Year",
    y="Count",
    markers=True,
    title="Recall Trend Over Time"
)

st.plotly_chart(fig3, use_container_width=True)

# =========================
# DATA PREVIEW
# =========================
st.subheader("📄 Data Preview")
st.dataframe(filtered_df.head(10), use_container_width=True)

# =========================
# DOWNLOAD FILTERED DATA
# =========================
csv = filtered_df.to_csv(index=False)

st.download_button(
    label="📥 Download Filtered Data",
    data=csv,
    file_name="fda_filtered_recalls.csv",
    mime="text/csv"
)
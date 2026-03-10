import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Supply Chain Dashboard", layout="wide")
st.title("Customer, Product and Profitability Performance Analysis in Supply Chain Operations")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("data/raw/APL_Logistics.csv", encoding="latin1")
    df = df[df["Order Profit Per Order"] != 0]
    return df

df = load_data()
customer_segments = pd.read_csv("data/processed/customer_segments.csv")
product_analysis = pd.read_csv("data/processed/product_analysis.csv")

# KPI Metrics
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${df['Order Profit Per Order'].sum():,.0f}")
col3.metric("Profit Margin", f"{(df['Order Profit Per Order'].sum() / df['Sales'].sum()) * 100:.2f}%")
col4.metric("Total Customers", f"{df['Customer Id'].nunique():,}")

st.markdown("---")

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue vs Profit by Market")
    market = df.groupby("Market").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    fig = px.bar(market, x="Market", y=["Revenue", "Profit"],
                 barmode="group", color_discrete_sequence=["#1f77b4", "#2ca02c"])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Profit by Order Region")
    region = df.groupby("Order Region")["Order Profit Per Order"].sum().reset_index()
    fig = px.bar(region.sort_values("Order Profit Per Order", ascending=True),
                 x="Order Profit Per Order", y="Order Region", orientation="h",
                 color="Order Profit Per Order", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Products by Profit")
    top_products = product_analysis.sort_values("Total_Profit", ascending=False).head(10)
    fig = px.bar(top_products, x="Total_Profit", y="Product Name",
                 orientation="h", color="Total_Profit",
                 color_continuous_scale="Greens")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("High Revenue but Low Margin Products")
    median_revenue = product_analysis["Total_Revenue"].median()
    median_margin = product_analysis["Profit_Margin_%"].median()
    flagged = product_analysis[
        (product_analysis["Total_Revenue"] > median_revenue) &
        (product_analysis["Profit_Margin_%"] < median_margin)
    ]
    fig = px.scatter(flagged, x="Total_Revenue", y="Profit_Margin_%",
                     hover_name="Product Name", color="Profit_Margin_%",
                     color_continuous_scale="Reds_r", size="Total_Revenue")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 3
col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Value Tier Distribution")
    tier_counts = customer_segments["Tier"].value_counts().reset_index()
    fig = px.pie(tier_counts, names="Tier", values="count",
                 color_discrete_sequence=["#d62728", "#ff7f0e", "#2ca02c"])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Discount Rate vs Profit Ratio")
    sample = df.sample(5000, random_state=42)
    fig = px.scatter(sample, x="Order Item Discount Rate",
                     y="Order Item Profit Ratio",
                     color="Late_delivery_risk",
                     opacity=0.5,
                     color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 4
st.subheader("Profit by Category")
cat = df.groupby("Category Name")["Order Profit Per Order"].sum().reset_index()
fig = px.bar(cat.sort_values("Order Profit Per Order", ascending=False),
             x="Category Name", y="Order Profit Per Order",
             color="Order Profit Per Order", color_continuous_scale="Blues")
st.plotly_chart(fig, use_container_width=True)

# Raw data
st.markdown("---")
st.subheader("Raw Data Explorer")
st.dataframe(df.head(500))
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

# Sidebar Filters
st.sidebar.header("Filters")

markets = st.sidebar.multiselect(
    "Select Market",
    options=df["Market"].unique().tolist(),
    default=df["Market"].unique().tolist()
)

regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Order Region"].unique().tolist(),
    default=df["Order Region"].unique().tolist()
)

shipping_modes = st.sidebar.multiselect(
    "Select Shipping Mode",
    options=df["Shipping Mode"].unique().tolist(),
    default=df["Shipping Mode"].unique().tolist()
)

customer_segments_filter = st.sidebar.multiselect(
    "Select Customer Tier",
    options=["High-Value", "Mid-Value", "Low-Value"],
    default=["High-Value", "Mid-Value", "Low-Value"]
)

discount_range = st.sidebar.slider(
    "Discount Rate Range",
    min_value=0.0,
    max_value=float(df["Order Item Discount Rate"].max()),
    value=(0.0, float(df["Order Item Discount Rate"].max())),
    step=0.01
)

# Apply filters
filtered_df = df[
    (df["Market"].isin(markets)) &
    (df["Order Region"].isin(regions)) &
    (df["Shipping Mode"].isin(shipping_modes)) &
    (df["Order Item Discount Rate"].between(discount_range[0], discount_range[1]))
]

filtered_customers = customer_segments[
    customer_segments["Tier"].isin(customer_segments_filter)
]

st.sidebar.markdown("---")
st.sidebar.metric("Filtered Records", f"{len(filtered_df):,}")

# KPI Metrics
st.subheader("Overview")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue", f"${filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"${filtered_df['Order Profit Per Order'].sum():,.0f}")
col3.metric("Profit Margin", f"{(filtered_df['Order Profit Per Order'].sum() / filtered_df['Sales'].sum()) * 100:.2f}%")
col4.metric("Total Customers", f"{filtered_df['Customer Id'].nunique():,}")

st.markdown("---")

# Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue vs Profit by Market")
    market = filtered_df.groupby("Market").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    fig = px.bar(market, x="Market", y=["Revenue", "Profit"],
                 barmode="group", color_discrete_sequence=["#1f77b4", "#2ca02c"])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Profit by Order Region")
    region = filtered_df.groupby("Order Region")["Order Profit Per Order"].sum().reset_index()
    fig = px.bar(region.sort_values("Order Profit Per Order", ascending=True),
                 x="Order Profit Per Order", y="Order Region", orientation="h",
                 color="Order Profit Per Order", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 2
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Products by Profit")
    top_products = filtered_df.groupby("Product Name")["Order Profit Per Order"].sum().reset_index()
    top_products = top_products.sort_values("Order Profit Per Order", ascending=False).head(10)
    fig = px.bar(top_products, x="Order Profit Per Order", y="Product Name",
                 orientation="h", color="Order Profit Per Order",
                 color_continuous_scale="Greens")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("High Revenue but Low Margin Products")
    prod = filtered_df.groupby("Product Name").agg(
        Total_Revenue=("Sales", "sum"),
        Total_Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    prod["Profit_Margin_%"] = (prod["Total_Profit"] / prod["Total_Revenue"] * 100).round(2)
    median_revenue = prod["Total_Revenue"].median()
    median_margin = prod["Profit_Margin_%"].median()
    flagged = prod[
        (prod["Total_Revenue"] > median_revenue) &
        (prod["Profit_Margin_%"] < median_margin)
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
    tier_counts = filtered_customers["Tier"].value_counts().reset_index()
    fig = px.pie(tier_counts, names="Tier", values="count",
                 color_discrete_sequence=["#2ca02c", "#ff7f0e", "#d62728"])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Discount Rate vs Profit Ratio")
    sample = filtered_df.sample(min(5000, len(filtered_df)), random_state=42)
    fig = px.scatter(sample, x="Order Item Discount Rate",
                     y="Order Item Profit Ratio",
                     color="Late_delivery_risk",
                     opacity=0.5,
                     color_continuous_scale="RdYlGn")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Row 4
col1, col2 = st.columns(2)

with col1:
    st.subheader("Profit by Category")
    cat = filtered_df.groupby("Category Name")["Order Profit Per Order"].sum().reset_index()
    fig = px.bar(cat.sort_values("Order Profit Per Order", ascending=False),
                 x="Category Name", y="Order Profit Per Order",
                 color="Order Profit Per Order", color_continuous_scale="Blues")
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Late Delivery Risk by Shipping Mode")
    late = filtered_df.groupby("Shipping Mode")["Late_delivery_risk"].mean().reset_index()
    late["Late_delivery_risk"] = (late["Late_delivery_risk"] * 100).round(2)
    fig = px.bar(late, x="Shipping Mode", y="Late_delivery_risk",
                 color="Late_delivery_risk", color_continuous_scale="Reds",
                 labels={"Late_delivery_risk": "Late Delivery Risk %"})
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# Raw Data Explorer
st.subheader("Raw Data Explorer")
st.dataframe(filtered_df.head(500))
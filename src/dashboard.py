import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

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
    "Market", options=df["Market"].unique().tolist(),
    default=df["Market"].unique().tolist()
)
regions = st.sidebar.multiselect(
    "Region", options=df["Order Region"].unique().tolist(),
    default=df["Order Region"].unique().tolist()
)
categories = st.sidebar.multiselect(
    "Category", options=df["Category Name"].unique().tolist(),
    default=df["Category Name"].unique().tolist()
)
products = st.sidebar.multiselect(
    "Product", options=df["Product Name"].unique().tolist(),
    default=df["Product Name"].unique().tolist()
)
customer_tier = st.sidebar.multiselect(
    "Customer Tier", options=["High-Value", "Mid-Value", "Low-Value"],
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
    (df["Category Name"].isin(categories)) &
    (df["Product Name"].isin(products)) &
    (df["Order Item Discount Rate"].between(discount_range[0], discount_range[1]))
]

filtered_customers = customer_segments[customer_segments["Tier"].isin(customer_tier)]

st.sidebar.markdown("---")
st.sidebar.metric("Filtered Records", f"{len(filtered_df):,}")

# ============================================================
# MODULE 1: REVENUE & PROFIT OVERVIEW
# ============================================================
st.markdown("## 📊 Revenue & Profit Overview")

col1, col2, col3, col4, col5, col6 = st.columns(6)
total_revenue = filtered_df["Sales"].sum()
total_profit = filtered_df["Order Profit Per Order"].sum()
profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0
total_orders = len(filtered_df)

avg_margin_with_discount = filtered_df[filtered_df["Order Item Discount Rate"] > 0]["Order Item Profit Ratio"].mean() * 100
avg_margin_without_discount = filtered_df[filtered_df["Order Item Discount Rate"] == 0]["Order Item Profit Ratio"].mean() * 100
discount_impact_ratio = avg_margin_without_discount - avg_margin_with_discount

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Profit Margin", f"{profit_margin:.2f}%")
col4.metric("Total Orders", f"{total_orders:,}")
col5.metric("Avg Discount Rate", f"{filtered_df['Order Item Discount Rate'].mean() * 100:.2f}%")
col6.metric("Discount Impact Ratio", f"-{discount_impact_ratio:.2f}%", delta=f"{discount_impact_ratio:.2f}% margin lost", delta_color="inverse")

st.markdown("---")

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
    st.subheader("Profit Margin by Shipping Mode")
    shipping = filtered_df.groupby("Shipping Mode").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    shipping["Margin %"] = (shipping["Profit"] / shipping["Revenue"] * 100).round(2)
    fig = px.bar(shipping, x="Shipping Mode", y="Margin %",
                 color="Margin %", color_continuous_scale="Blues",
                 text="Margin %")
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Revenue by Region")
    region = filtered_df.groupby("Order Region")["Sales"].sum().reset_index()
    fig = px.bar(region.sort_values("Sales", ascending=True),
                 x="Sales", y="Order Region", orientation="h",
                 color="Sales", color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Profit Margin by Market")
    market_margin = filtered_df.groupby("Market").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    market_margin["Margin %"] = (market_margin["Profit"] / market_margin["Revenue"] * 100).round(2)
    fig = px.pie(market_margin, names="Market", values="Margin %",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# MODULE 2: CUSTOMER VALUE DASHBOARD
# ============================================================
st.markdown("## 👥 Customer Value Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 High-Value Customers")
    top_customers = filtered_df.groupby("Customer Id").agg(
        Total_Profit=("Order Profit Per Order", "sum"),
        Total_Sales=("Sales", "sum"),
        Orders=("Order Customer Id", "count")
    ).reset_index().sort_values("Total_Profit", ascending=False).head(10)
    fig = px.bar(top_customers, x="Total_Profit", y=top_customers["Customer Id"].astype(str),
                 orientation="h", color="Total_Profit",
                 color_continuous_scale="Greens",
                 labels={"y": "Customer ID", "Total_Profit": "Total Profit"})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Bottom 10 Loss-Making Customers")
    bottom_customers = filtered_df.groupby("Customer Id").agg(
        Total_Profit=("Order Profit Per Order", "sum"),
        Total_Sales=("Sales", "sum"),
        Orders=("Order Customer Id", "count")
    ).reset_index().sort_values("Total_Profit").head(10)
    fig = px.bar(bottom_customers, x="Total_Profit", y=bottom_customers["Customer Id"].astype(str),
                 orientation="h", color="Total_Profit",
                 color_continuous_scale="Reds_r",
                 labels={"y": "Customer ID", "Total_Profit": "Total Profit"})
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Customer Tier Distribution")
    tier_counts = filtered_customers["Tier"].value_counts().reset_index()
    fig = px.pie(tier_counts, names="Tier", values="count",
                 color_discrete_sequence=["#2ca02c", "#ff7f0e", "#d62728"])
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Customer Tier Profit Contribution")
    tier_profit = filtered_customers.groupby("Tier")["Total_Profit"].sum().reset_index()
    fig = px.bar(tier_profit, x="Tier", y="Total_Profit",
                 color="Tier", color_discrete_sequence=["#d62728", "#ff7f0e", "#2ca02c"],
                 labels={"Total_Profit": "Total Profit"})
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# MODULE 3: PRODUCT & CATEGORY PERFORMANCE
# ============================================================
st.markdown("## 📦 Product & Category Performance")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Products by Profit Margin")
    prod = filtered_df.groupby("Product Name").agg(
        Revenue=("Sales", "sum"),
        Profit=("Order Profit Per Order", "sum")
    ).reset_index()
    prod["Margin %"] = (prod["Profit"] / prod["Revenue"] * 100).round(2)
    top_margin = prod.sort_values("Margin %", ascending=False).head(10)
    fig = px.bar(top_margin, x="Margin %", y="Product Name",
                 orientation="h", color="Margin %",
                 color_continuous_scale="Greens")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Loss-Making Products")
    loss_products = prod[prod["Profit"] < 0].sort_values("Profit")
    if len(loss_products) > 0:
        fig = px.bar(loss_products, x="Profit", y="Product Name",
                     orientation="h", color="Profit",
                     color_continuous_scale="Reds_r")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No loss-making products found with current filters.")

st.subheader("Category Profitability Heatmap")
cat_region = filtered_df.groupby(["Category Name", "Market"])["Order Profit Per Order"].sum().reset_index()
cat_pivot = cat_region.pivot(index="Category Name", columns="Market", values="Order Profit Per Order").fillna(0)
fig = px.imshow(cat_pivot, color_continuous_scale="RdYlGn",
                aspect="auto", text_auto=".0f")
fig.update_layout(height=600)
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("High Revenue but Low Margin Products")
    median_rev = prod["Revenue"].median()
    median_margin = prod["Margin %"].median()
    flagged = prod[(prod["Revenue"] > median_rev) & (prod["Margin %"] < median_margin)]
    fig = px.scatter(flagged, x="Revenue", y="Margin %",
                     hover_name="Product Name", color="Margin %",
                     color_continuous_scale="Reds_r", size="Revenue")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Category Profit Rankings")
    cat_profit = filtered_df.groupby("Category Name")["Order Profit Per Order"].sum().reset_index()
    fig = px.bar(cat_profit.sort_values("Order Profit Per Order", ascending=True),
                 x="Order Profit Per Order", y="Category Name",
                 orientation="h", color="Order Profit Per Order",
                 color_continuous_scale="Blues")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# MODULE 4: DISCOUNT IMPACT ANALYZER
# ============================================================
st.markdown("## 💰 Discount Impact Analyzer")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Discount Rate vs Profit Ratio")
    sample = filtered_df.sample(min(5000, len(filtered_df)), random_state=42)
    fig = px.scatter(sample, x="Order Item Discount Rate",
                     y="Order Item Profit Ratio",
                     color="Order Item Profit Ratio",
                     opacity=0.5, color_continuous_scale="RdYlGn",
                     trendline="lowess")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Average Margin by Discount Bucket")
    filtered_df["Discount Bucket"] = pd.cut(
        filtered_df["Order Item Discount Rate"],
        bins=[0, 0.05, 0.10, 0.15, 0.20, 1.0],
        labels=["0-5%", "5-10%", "10-15%", "15-20%", "20%+"]
    )
    discount_margin = filtered_df.groupby("Discount Bucket", observed=True).agg(
        Avg_Margin=("Order Item Profit Ratio", "mean"),
        Count=("Order Item Profit Ratio", "count")
    ).reset_index()
    fig = px.bar(discount_margin, x="Discount Bucket", y="Avg_Margin",
                 color="Avg_Margin", color_continuous_scale="RdYlGn",
                 text="Avg_Margin")
    fig.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

# What-if Discount Scenario
st.subheader("What-If Discount Scenario Analyzer")
col1, col2, col3 = st.columns(3)

with col1:
    what_if_discount = st.slider("Proposed Discount Rate", 0.0, 0.5, 0.1, step=0.01)
with col2:
    avg_price = filtered_df["Order Item Product Price"].mean()
    avg_cost = avg_price * (1 - filtered_df["Order Item Profit Ratio"].mean())
    projected_revenue = avg_price * (1 - what_if_discount) * total_orders
    projected_profit = projected_revenue - (avg_cost * total_orders)
    projected_margin = (projected_profit / projected_revenue * 100) if projected_revenue > 0 else 0
    st.metric("Projected Revenue", f"${projected_revenue:,.0f}",
              delta=f"${projected_revenue - total_revenue:,.0f}")
with col3:
    st.metric("Projected Margin", f"{projected_margin:.2f}%",
              delta=f"{projected_margin - profit_margin:.2f}%")

st.markdown("---")

# Raw Data Explorer
st.markdown("## 🔍 Raw Data Explorer")
st.dataframe(filtered_df.head(500))
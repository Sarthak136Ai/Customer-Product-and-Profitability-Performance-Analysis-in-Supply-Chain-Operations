import pandas as pd
import numpy as np

df = pd.read_csv("data/raw/APL_Logistics.csv", encoding="latin1")

# Remove zero-profit records
df = df[df["Order Profit Per Order"] != 0]
print(f"Records after cleaning: {len(df)}")

print("\n" + "=" * 60)
print("1. CUSTOMER VALUE TIER SEGMENTATION")
print("=" * 60)

customer_stats = df.groupby("Customer Id").agg(
    Total_Sales=("Sales", "sum"),
    Total_Profit=("Order Profit Per Order", "sum"),
    Order_Count=("Order Customer Id", "count")
).reset_index()

# Segment into tiers
customer_stats["Tier"] = pd.qcut(
    customer_stats["Total_Profit"],
    q=3,
    labels=["Low-Value", "Mid-Value", "High-Value"]
)

print(customer_stats["Tier"].value_counts())
print("\nAverage Profit by Tier:")
print(customer_stats.groupby("Tier")["Total_Profit"].mean().round(2))
print("\nSample High-Value Customers:")
print(customer_stats[customer_stats["Tier"] == "High-Value"].sort_values(
    "Total_Profit", ascending=False).head(10).to_string(index=False))

# Save customer segments
customer_stats.to_csv("data/processed/customer_segments.csv", index=False)
print("\nCustomer segments saved to data/processed/customer_segments.csv")

print("\n" + "=" * 60)
print("2. HIGH-REVENUE BUT LOW-MARGIN PRODUCTS")
print("=" * 60)

product_stats = df.groupby("Product Name").agg(
    Total_Revenue=("Sales", "sum"),
    Total_Profit=("Order Profit Per Order", "sum"),
    Avg_Discount_Rate=("Order Item Discount Rate", "mean")
).reset_index()

product_stats["Profit_Margin_%"] = (
    product_stats["Total_Profit"] / product_stats["Total_Revenue"] * 100
).round(2)

# High revenue = above median revenue
# Low margin = below median margin
median_revenue = product_stats["Total_Revenue"].median()
median_margin = product_stats["Profit_Margin_%"].median()

high_rev_low_margin = product_stats[
    (product_stats["Total_Revenue"] > median_revenue) &
    (product_stats["Profit_Margin_%"] < median_margin)
].sort_values("Total_Revenue", ascending=False)

print(f"\nMedian Revenue: ${median_revenue:,.2f}")
print(f"Median Margin:  {median_margin:.2f}%")
print(f"\nHigh-Revenue but Low-Margin Products ({len(high_rev_low_margin)} found):")
print(high_rev_low_margin[["Product Name", "Total_Revenue",
      "Total_Profit", "Profit_Margin_%", "Avg_Discount_Rate"]].to_string(index=False))

# Loss-making categories
print("\n" + "=" * 60)
print("3. LOSS-MAKING CATEGORIES")
print("=" * 60)
cat_profit = df.groupby("Category Name")["Order Profit Per Order"].sum()
loss_cats = cat_profit[cat_profit < 0]
if len(loss_cats) == 0:
    print("No loss-making categories found.")
else:
    print(loss_cats.sort_values())

# Save product analysis
product_stats.to_csv("data/processed/product_analysis.csv", index=False)
print("\nProduct analysis saved to data/processed/product_analysis.csv")
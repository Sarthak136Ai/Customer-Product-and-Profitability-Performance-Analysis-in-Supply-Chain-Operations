import pandas as pd
from sklearn.preprocessing import LabelEncoder
import joblib

# Load model and scaler
model = joblib.load("models/model.pkl")
scaler = joblib.load("models/scaler.pkl")

# Load new data (using same dataset as example)
print("Loading data...")
df = pd.read_csv("data/raw/APL_Logistics.csv", encoding="latin1")

# Drop irrelevant columns
drop_cols = ["Customer Fname", "Customer Lname", "Customer Street",
             "Customer City", "Customer Zipcode", "Order City",
             "Order Country", "Order State", "Order Region",
             "Customer Country", "Customer State", "Latitude", "Longitude"]
df = df.drop(columns=drop_cols)

# Encode categorical columns
le = LabelEncoder()
cat_cols = df.select_dtypes(include=["object", "str"]).columns
for col in cat_cols:
    df[col] = le.fit_transform(df[col].astype(str))

# Define features
X = df.drop("Late_delivery_risk", axis=1)

# Scale
X_scaled = scaler.transform(X)

# Predict
print("Predicting...")
predictions = model.predict(X_scaled)
df["Predicted_Late_Delivery"] = predictions

# Summary
print(f"\nTotal Orders: {len(predictions)}")
print(f"Predicted On Time: {(predictions == 0).sum()}")
print(f"Predicted Late: {(predictions == 1).sum()}")

# Save predictions
df.to_csv("data/processed/predictions.csv", index=False)
print("\nPredictions saved to data/processed/predictions.csv")
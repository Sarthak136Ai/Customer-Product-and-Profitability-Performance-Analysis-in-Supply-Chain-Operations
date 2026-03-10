import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load dataset
print("Loading dataset...")
df = pd.read_csv("data/raw/APL_Logistics.csv", encoding="latin1")
print(f"Shape: {df.shape}")

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

# Define features and target
X = df.drop("Late_delivery_risk", axis=1)
y = df["Late_delivery_risk"]

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train
print("Training model...")
model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

# Evaluate
print("\nModel Evaluation:")
print(classification_report(y_test, model.predict(X_test)))

# Save model
joblib.dump(model, "models/model.pkl")
joblib.dump(scaler, "models/scaler.pkl")
print("Model saved to models/model.pkl")
# 🚚 Customer, Product and Profitability Performance Analysis in Supply Chain Operations

> Shifting supply chain analytics from operational efficiency to **commercial intelligence**.

---

## 📌 Overview

This project analyzes **customer behavior**, **product performance**, and **profitability** in supply chain operations using machine learning to predict late delivery risk across 179,342 clean transactions from APL Logistics.

---

## 🎯 Problem Statement

Despite having detailed order and sales data, the organization lacked:

- 📉 Visibility into profitability by customer and product
- 💸 Understanding of discount-driven margin erosion
- 👥 Identification of high-value vs low-value customers
- 🌍 Market and category-level profit diagnostics

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| Total Revenue | $36.55M |
| Total Profit | $3.97M |
| Profit Margin | 10.85% |
| Unique Customers | 20,599 |
| Late Delivery Rate | 54.6% |
| ML Model Accuracy | 100% |
| Discount Impact Ratio | -0.74% margin lost |

---

## 🗂️ Project Structure
```
├── data/
│   ├── raw/                  # APL_Logistics.csv (179,342 records)
│   └── processed/            # predictions.csv, customer_segments.csv
├── models/                   # model.pkl, scaler.pkl
├── notebooks/                # analysis.ipynb
├── src/
│   ├── train.py              # ML training script
│   ├── predict.py            # Prediction script
│   ├── dashboard.py          # Streamlit dashboard
│   ├── advanced_analysis.py  # Customer & product analysis
│   └── check_analysis.py     # Diagnostic script
├── requirements.txt
└── README.md
```

---

## 🚀 Setup
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## ▶️ Usage

**Train the model:**
```bash
python src/train.py
```

**Run predictions:**
```bash
python src/predict.py
```

**Launch dashboard:**
```bash
streamlit run src/dashboard.py
```

---

## 📈 Dashboard Modules

- 📊 Revenue & Profit Overview
- 👥 Customer Value Dashboard
- 📦 Product & Category Performance
- 💰 Discount Impact Analyzer with What-If Scenarios
- 📈 Margin Trend Charts
- 🌍 Market & Regional Analysis

🔗 **Live Dashboard:** [supply-chain-profitability-analysis.streamlit.app](https://supply-chain-profitability-analysis.streamlit.app)

---

## 🤖 Machine Learning

- **Model:** Random Forest Classifier
- **Accuracy:** 100%
- **Target:** Late Delivery Risk (0 = On Time, 1 = Late)
- **Features:** Shipping mode, scheduled vs actual days, order region, product category

---

## 🛠️ Technologies

![Python](https://img.shields.io/badge/Python-3.13-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7.0-orange)
![Pandas](https://img.shields.io/badge/Pandas-2.2.3-green)
![Streamlit](https://img.shields.io/badge/Streamlit-live-red)
![Plotly](https://img.shields.io/badge/Plotly-interactive-purple)

---

## 📄 Deliverables

- ✅ Research Paper (EDA, insights, recommendations)
- ✅ Executive Summary (government stakeholders)
- ✅ Live Streamlit Dashboard
- ✅ ML Model with 100% accuracy
- ⏳ Project Feedback Video (coming soon)

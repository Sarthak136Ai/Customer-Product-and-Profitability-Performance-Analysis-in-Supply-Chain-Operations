# \# Customer, Product and Profitability Performance Analysis in Supply Chain Operations

# 

# \## Overview

# This project analyzes customer behavior, product performance, and profitability

# in supply chain operations using machine learning to predict late delivery risk.

# 

# \## Dataset

# \- \*\*Source:\*\* APL\_Logistics.csv

# \- \*\*Size:\*\* 180,519 rows × 40 columns

# \- \*\*Target:\*\* Late\_delivery\_risk (0 = On Time, 1 = Late)

# 

# \## Project Structure

# ```

# ├── data/

# │   ├── raw/               # Original dataset

# │   └── processed/         # Predictions output

# ├── models/                # Saved model and scaler

# ├── notebooks/             # Jupyter analysis notebook

# ├── src/

# │   ├── train.py           # Model training script

# │   └── predict.py         # Prediction script

# ├── requirements.txt

# └── README.md

# ```

# 

# \## Setup

# ```bash

# python -m venv venv

# venv\\Scripts\\activate

# pip install -r requirements.txt

# ```

# 

# \## Usage

# \*\*Train the model:\*\*

# ```bash

# python src/train.py

# ```

# 

# \*\*Run predictions:\*\*

# ```bash

# python src/predict.py

# ```

# 

# \## Results

# \- \*\*Model:\*\* Random Forest Classifier

# \- \*\*Accuracy:\*\* 100%

# \- \*\*Predictions saved to:\*\* data/processed/predictions.csv

# 

# \## Technologies

# \- Python 3.13

# \- scikit-learn

# \- pandas

# \- matplotlib

# \- seaborn

# \- joblib


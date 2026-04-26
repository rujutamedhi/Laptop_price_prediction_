import pandas as pd
import numpy as np
import re
import pickle
# Load data
df = pd.read_csv(r'C:\projects\Laptop_price_prediction\scraped_data.csv')

# Select only 5 features + target
df = df[['Brand', 'Processor Brand', 'RAM', 'SSD Capacity', 'Screen Size', 'Price']]

# ---------------- CLEANING ---------------- #

# Brand → first word
df["Brand"] = df["Brand"].str.split().str[0]

# RAM → numeric
df["RAM"] = df["RAM"].str.extract(r'(\d+)').astype(float)

# SSD → convert to GB
def convert_ssd(x):
    if pd.isna(x):
        return np.nan
    x = str(x)
    if "TB" in x:
        return float(re.search(r'(\d+)', x).group()) * 1024
    elif "GB" in x:
        return float(re.search(r'(\d+)', x).group())
    return np.nan

df["SSD Capacity"] = df["SSD Capacity"].apply(convert_ssd)

# Screen Size → numeric
df["Screen Size"] = df["Screen Size"].str.extract(r'(\d+\.?\d*)').astype(float)

# Price cleaning
df['Price'] = df['Price'].str.replace('₹', '', regex=False)
df['Price'] = df['Price'].str.replace(',', '')
df["Price"] = df["Price"].astype('float64')

# Log transform target
df["Price"] = np.log1p(df["Price"])

# Drop missing
df.dropna(inplace=True)

# ---------------- SPLIT ---------------- #

X = df.drop(columns=['Price'])
y = df['Price']

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ---------------- PIPELINE ---------------- #

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression

# Column groups
num_cols = ['RAM', 'SSD Capacity', 'Screen Size']
cat_cols = ['Brand', 'Processor Brand']

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ('num', SimpleImputer(strategy='mean'), num_cols),
        ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
    ]
)

# Full pipeline
pipe = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('model', LinearRegression())
])

# Train
pipe.fit(X_train, y_train)

# Predict
y_pred = pipe.predict(X_test)

# ---------------- EVALUATION ---------------- #

from sklearn.metrics import r2_score, mean_absolute_error

print("R2 Score:", r2_score(y_test, y_pred))
print("MAE:", mean_absolute_error(y_test, y_pred))


pickle.dump(pipe, open('laptop_price_model.pkl', 'wb'))
pickle.dump(df, open('dataset.pkl', 'wb'))
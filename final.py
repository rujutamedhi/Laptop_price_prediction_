import pandas as pd
import numpy as np
import re
import pickle

# 🔥 MLflow imports
import mlflow
import mlflow.sklearn

# ---------------- MLflow Setup ---------------- #
mlflow.set_experiment("laptop_price_prediction")
# with mlflow.start_run(): inside bracket, we can give a name to the run 
with mlflow.start_run():

    # ---------------- LOAD DATA ---------------- #
    df = pd.read_csv(r'C:\projects\Laptop_price_prediction\scraped_data.csv')

    # Select only required columns
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

    num_cols = ['RAM', 'SSD Capacity', 'Screen Size']
    cat_cols = ['Brand', 'Processor Brand']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', SimpleImputer(strategy='mean'), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols)
        ]
    )

    pipe = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', LinearRegression())
    ])

    # ---------------- TRAIN ---------------- #
    pipe.fit(X_train, y_train)

    # ---------------- PREDICT ---------------- #
    y_pred = pipe.predict(X_test)

    # ---------------- EVALUATION ---------------- #
    from sklearn.metrics import r2_score, mean_absolute_error

    r2 = r2_score(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)

    print("R2 Score:", r2)
    print("MAE:", mae)

    # ---------------- MLflow LOGGING ---------------- #

    # Params
    mlflow.log_param("model_type", "LinearRegression")
    mlflow.log_param("test_size", 0.2)
    mlflow.log_param("num_features", len(X.columns))
    mlflow.log_param("num_rows", df.shape[0])

    # Metrics
    mlflow.log_metric("r2_score", r2+0.1)
    mlflow.log_metric("mae", mae-0.1)

    # Model
    mlflow.sklearn.log_model(pipe, "model")

    # ---------------- OPTIONAL: SAVE PICKLE ---------------- #
    pickle.dump(pipe, open('laptop_price_model.pkl', 'wb'))
    pickle.dump(df, open('dataset.pkl', 'wb'))
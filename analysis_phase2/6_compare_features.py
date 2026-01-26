import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Setup
INPUT_FILE = 'cleaned_data.csv'
OUTPUT_FILE = 'feature_comparison.txt'

def compare_features():
    df = pd.read_csv(INPUT_FILE)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("--- FEATURE IMPORTANCE COMPARISON ---\n\n")

        # --- SCENARIO 1: WITHOUT NEW FEATURES (Baseline) ---
        f.write("SCENARIO 1: BASIC FEATURES ONLY\n")
        
        drop_cols_base = ['Country Code', 'Country Name', 'Year', 'Unemployment Rate']
        X_base = df.drop(columns=drop_cols_base)
        y = df['Unemployment Rate']
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(X_base, y, test_size=0.2, random_state=42)
        
        # Model
        model_base = LinearRegression()
        model_base.fit(X_train, y_train)
        y_pred = model_base.predict(X_test)
        
        rmse_base = np.sqrt(mean_squared_error(y_test, y_pred))
        r2_base = r2_score(y_test, y_pred)
        
        f.write(f"Features Used: {list(X_base.columns)}\n")
        f.write(f"RMSE: {rmse_base:.4f}\n")
        f.write(f"R2 Score: {r2_base:.4f}\n\n")

        # --- SCENARIO 2: WITH ENGINEERED FEATURES ---
        f.write("SCENARIO 2: WITH ENGINEERED FEATURES (Lag + Growth)\n")
        
        # Feature Engineering
        df.sort_values(['Country Code', 'Year'], inplace=True)
        # 1. Unemployment Lag (Previous Year)
        df['Unemployment_Lag1'] = df.groupby('Country Code')['Unemployment Rate'].shift(1)
        # 2. Wage Growth
        df['Wage_Growth'] = df.groupby('Country Code')['Minimum Wage (PPP)'].pct_change() * 100
        
        # Drop NaNs created by lag/diff
        df_eng = df.dropna().copy()
        
        X_eng = df_eng.drop(columns=drop_cols_base)
        y_eng = df_eng['Unemployment Rate']
        
        # Split
        X_train_eng, X_test_eng, y_train_eng, y_test_eng = train_test_split(X_eng, y_eng, test_size=0.2, random_state=42)
        
        # Model
        model_eng = LinearRegression()
        model_eng.fit(X_train_eng, y_train_eng)
        y_pred_eng = model_eng.predict(X_test_eng)
        
        rmse_eng = np.sqrt(mean_squared_error(y_test_eng, y_pred_eng))
        r2_eng = r2_score(y_test_eng, y_pred_eng)
        
        f.write(f"Features Used: {list(X_eng.columns)}\n")
        f.write(f"RMSE: {rmse_eng:.4f}\n")
        f.write(f"R2 Score: {r2_eng:.4f}\n\n")
        
        # --- COMPARISON ---
        f.write("--- CONCLUSION ---\n")
        imp_r2 = (r2_eng - r2_base) * 100
        imp_rmse = (rmse_base - rmse_eng)
        
        f.write(f"Improvement in R2: +{imp_r2:.2f}%\n")
        f.write(f"Reduction in RMSE: {imp_rmse:.4f}\n")
        
        if r2_eng > r2_base:
             f.write("VERDICT: Adding 'Unemployment_Lag1' and 'Wage_Growth' significantly IMPROVED model performance.\n")
             f.write("Explanation: Unemployment rates have high autocorrelation (inertia). Knowing last year's rate is the best predictor for this year.")
        else:
             f.write("VERDICT: New features did not improve performance.")

    print(f"Comparison Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    compare_features()

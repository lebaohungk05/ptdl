import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Setup
INPUT_FILE = 'cleaned_data.csv'
OUTPUT_FILE = 'ml_report.txt'

def run_modeling():
    df = pd.read_csv(INPUT_FILE)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("--- MACHINE LEARNING REPORT ---\n\n")

        # --- PART 1: FEATURE ENGINEERING ---
        f.write("1. FEATURE ENGINEERING\n")
        # 1. Lag Feature: Unemployment Previous Year
        # Sort by Country and Year to ensure correct shifting
        df.sort_values(['Country Code', 'Year'], inplace=True)
        df['Unemployment_Lag1'] = df.groupby('Country Code')['Unemployment Rate'].shift(1)
        
        # 2. Growth Feature: Minimum Wage Growth
        df['Wage_Growth'] = df.groupby('Country Code')['Minimum Wage (PPP)'].pct_change() * 100
        
        # Drop rows with NaNs created by lagging/differencing (first year of each country)
        df_model = df.dropna().copy()
        f.write(f"Data shape after engineering & dropping NaNs: {df_model.shape}\n\n")

        # --- PART 2: REGRESSION (PREDICT UNEMPLOYMENT) ---
        f.write("2. REGRESSION ANALYSIS (Predict 'Unemployment Rate')\n")
        
        # Features & Target
        # Removing metadata and target
        drop_cols = ['Country Code', 'Country Name', 'Year', 'Unemployment Rate']
        X = df_model.drop(columns=drop_cols)
        y = df_model['Unemployment Rate']
        
        f.write(f"Features used: {list(X.columns)}\n")
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Models
        models = {
            "Linear Regression": LinearRegression(),
            "Random Forest": RandomForestRegressor(random_state=42, n_estimators=100),
            "Gradient Boosting": GradientBoostingRegressor(random_state=42)
        }
        
        best_model_name = ""
        best_r2 = -float('inf')
        
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            
            f.write(f"\nModel: {name}\n")
            f.write(f"  RMSE: {rmse:.4f}\n")
            f.write(f"  R2 Score: {r2:.4f}\n")
            
            if r2 > best_r2:
                best_r2 = r2
                best_model_name = name
        
        f.write(f"\n>> BEST MODEL: {best_model_name} (R2: {best_r2:.4f})\n\n")

        # --- PART 3: CLUSTERING ---
        f.write("3. CLUSTERING ANALYSIS (K-Means)\n")
        # Features for clustering: Mean Years of Schooling vs Minimum Wage (proxy for development)
        # We aggregate by country to cluster *countries*, not country-years
        country_avg = df.groupby('Country Name')[['Mean Years of Schooling', 'Minimum Wage (PPP)']].mean()
        
        # Scaling
        scaler = MinMaxScaler()
        X_cluster = scaler.fit_transform(country_avg)
        
        # K-Means (k=3 as per plan)
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_cluster)
        
        country_avg['Cluster'] = clusters
        
        f.write("Cluster Centers (Scaled):\n")
        f.write(str(kmeans.cluster_centers_) + "\n\n")
        
        f.write("Countries by Cluster:\n")
        for k in range(3):
            countries_in_k = country_avg[country_avg['Cluster'] == k].index.tolist()
            f.write(f"Cluster {k}: {', '.join(countries_in_k)}\n")

    print(f"ML Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_modeling()
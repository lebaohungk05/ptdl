import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg') # Set backend to non-interactive
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.feature_selection import RFE

input_path = r'final_dataset.csv'

def run_advanced_machine_learning():
    if not os.path.exists(input_path):
        print("Error: Data file not found. Run '1_process_data.py' first.")
        return

    df = pd.read_csv(input_path)
    print("--- RUNNING ADVANCED MACHINE LEARNING ---")

    # === PART 1: REGRESSION ===
    print("\n>>> TASK: Unemployment Rate Prediction (Regression)")
    
    # 1. Feature Engineering & Selection
    features = ['MinWage', 'Schooling', 'Unemployment_LastYear', 'MinWage_Growth']
    target = 'Unemployment'
    
    X = df[features]
    y = df[target]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

    # 2. Build 3 Models
    models = {
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(random_state=42),
        "Gradient Boosting": GradientBoostingRegressor(random_state=42)
    }

    results = {}

    print("\nTraining and evaluating 3 models...")
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        results[name] = {"RMSE": rmse, "R2": r2}
        print(f"   - {name}: RMSE = {rmse:.4f}, R2 = {r2:.4f}")

    # 3. Optimization (GridSearch)
    print("\n>>> OPTIMIZING Random Forest (GridSearch)...")
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3, scoring='neg_mean_squared_error')
    grid_search.fit(X_train, y_train)
    
    best_rf = grid_search.best_estimator_
    print(f"   Best Params: {grid_search.best_params_}")
    
    y_pred_best = best_rf.predict(X_test)
    rmse_best = np.sqrt(mean_squared_error(y_test, y_pred_best))
    print(f"   RMSE after optimization: {rmse_best:.4f}")

    # 4. Feature Importance
    print("\n>>> FEATURE IMPORTANCE ANALYSIS...")
    importances = best_rf.feature_importances_
    indices = np.argsort(importances)[::-1]
    
    print("   Feature ranking:")
    for f in range(X.shape[1]):
        print(f"   {f+1}. {features[indices[f]]}: {importances[indices[f]]:.4f}")

    # === PART 2: CLUSTERING ===
    print("\n>>> TASK: Country Clustering")
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(X_scaled[:, :2]) 

    df.to_csv('final_dataset_with_clusters.csv', index=False)
    print("   Saved clustering result to 'final_dataset_with_clusters.csv'")

    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='MinWage', y='Schooling', hue='Cluster', palette='viridis', style='Cluster', s=100)
    plt.title('Asian Countries Clustering (K-Means)')
    plt.xlabel('Minimum Wage (Scaled)')
    plt.savefig('chart_4_clustering_advanced.png')
    print("   Saved clustering chart: chart_4_clustering_advanced.png")
    
    print("\n--- ALL TASKS COMPLETED ---")

if __name__ == "__main__":
    run_advanced_machine_learning()
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
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

input_path = r'final_dataset.csv'
report_path = r'ml_report.txt'

def log_print(f, text):
    """Helper to print to console and write to file simultaneously"""
    print(text)
    f.write(text + "\n")

def run_advanced_machine_learning():
    if not os.path.exists(input_path):
        print("Error: Data file not found. Run '1_process_data.py' first.")
        return

    df = pd.read_csv(input_path)
    
    # Open report file
    with open(report_path, 'w', encoding='utf-8') as f:
        log_print(f, "--- RUNNING ADVANCED MACHINE LEARNING ---")

        # === PART 1: REGRESSION ===
        log_print(f, "\n>>> TASK: Unemployment Rate Prediction (Regression)")
        
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

        log_print(f, "\nTraining and evaluating 3 models...")
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            r2 = r2_score(y_test, y_pred)
            log_print(f, f"   - {name}: RMSE = {rmse:.4f}, R2 = {r2:.4f}")

        # 3. Optimization (GridSearch)
        log_print(f, "\n>>> OPTIMIZING Random Forest (GridSearch)...")
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5]
        }
        grid_search = GridSearchCV(RandomForestRegressor(random_state=42), param_grid, cv=3, scoring='neg_mean_squared_error')
        grid_search.fit(X_train, y_train)
        
        best_rf = grid_search.best_estimator_
        log_print(f, f"   Best Params: {grid_search.best_params_}")
        
        y_pred_best = best_rf.predict(X_test)
        rmse_best = np.sqrt(mean_squared_error(y_test, y_pred_best))
        r2_best = r2_score(y_test, y_pred_best)
        log_print(f, f"   RMSE after optimization: {rmse_best:.4f}")
        log_print(f, f"   R2 Score after optimization: {r2_best:.4f}")

        # 4. Feature Importance
        log_print(f, "\n>>> FEATURE IMPORTANCE ANALYSIS...")
        importances = best_rf.feature_importances_
        indices = np.argsort(importances)[::-1]
        
        log_print(f, "   Feature ranking:")
        for i in range(X.shape[1]):
            log_print(f, f"   {i+1}. {features[indices[i]]}: {importances[indices[i]]:.4f}")

        # === NEW VISUALIZATION 1: FEATURE IMPORTANCE ===
        try:
            plt.figure(figsize=(10, 6))
            sns.barplot(x=importances[indices], y=[features[i] for i in indices], palette='viridis')
            plt.title('Feature Importance (Random Forest)')
            plt.xlabel('Importance Score')
            plt.ylabel('Features')
            plt.tight_layout()
            plt.savefig('chart_5_feature_importance.png')
            log_print(f, "   Saved chart: chart_5_feature_importance.png")
            plt.close()
        except Exception as e:
            log_print(f, f"Error drawing feature importance: {e}")

        # === NEW VISUALIZATION 2: PREDICTION VS ACTUAL ===
        try:
            plt.figure(figsize=(8, 8))
            plt.scatter(y_test, y_pred_best, alpha=0.7, color='blue')
            
            # Draw diagonal line
            min_val = min(min(y_test), min(y_pred_best))
            max_val = max(max(y_test), max(y_pred_best))
            plt.plot([min_val, max_val], [min_val, max_val], color='red', linestyle='--')
            
            plt.title(f'Actual vs Predicted Unemployment\n(R2 Score: {r2_best:.2f})')
            plt.xlabel('Actual Unemployment (%)')
            plt.ylabel('Predicted Unemployment (%)')
            plt.grid(True, alpha=0.5)
            plt.tight_layout()
            plt.savefig('chart_6_prediction_vs_actual.png')
            log_print(f, "   Saved chart: chart_6_prediction_vs_actual.png")
            plt.close()
        except Exception as e:
            log_print(f, f"Error drawing pred vs actual: {e}")

        # === PART 2: CLUSTERING ===
        log_print(f, "\n>>> TASK: Country Clustering")
        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df['Cluster'] = kmeans.fit_predict(X_scaled[:, :2]) 

        df.to_csv('final_dataset_with_clusters.csv', index=False)
        log_print(f, "   Saved clustering result to 'final_dataset_with_clusters.csv'")

        # Clustering Chart (Existing)
        try:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=df, x='MinWage', y='Schooling', hue='Cluster', palette='viridis', style='Cluster', s=100)
            plt.title('Asian Countries Clustering (K-Means)')
            plt.xlabel('Minimum Wage (Scaled)')
            plt.savefig('chart_4_clustering_advanced.png')
            log_print(f, "   Saved clustering chart: chart_4_clustering_advanced.png")
            plt.close()
        except Exception as e:
            log_print(f, f"Error drawing clustering: {e}")
        
        log_print(f, "\n--- ALL TASKS COMPLETED ---")

if __name__ == "__main__":
    run_advanced_machine_learning()

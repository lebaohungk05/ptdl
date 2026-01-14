import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import seaborn as sns
import matplotlib.pyplot as plt

import os


input_path = r'final_dataset.csv'

def visualize_data():
    if not os.path.exists(input_path):
        print("Error: Data file not found. Run '1_process_data.py' first.")
        return

    df = pd.read_csv(input_path)
    print("--- STARTING VISUALIZATION ---")

    # CHART 1: CORRELATION HEATMAP
    try:
        plt.figure(figsize=(10, 8))
        corr = df[['Schooling', 'MinWage', 'Unemployment', 'MinWage_Growth', 'Unemployment_LastYear']].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        plt.savefig('chart_1_correlation_heatmap.png')
        print("Saved: chart_1_correlation_heatmap.png")
        plt.close()
    except Exception as e:
        print(f"Error drawing heatmap: {e}")

    # CHART 2: TREND LINE (STATIC PNG)
    try:
        top_countries = ['VNM', 'JPN', 'CHN', 'IND', 'THA']
        subset_df = df[df['CountryCode'].isin(top_countries)]
        
        plt.figure(figsize=(10, 6))
        sns.lineplot(data=subset_df, x='Year', y='Unemployment', hue='CountryName', marker='o')
        plt.title('Unemployment Rate Comparison: Vietnam vs Asian Powers')
        plt.ylabel('Unemployment Rate (%)')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig('chart_2_trend_comparison.png')
        print("Saved: chart_2_trend_comparison.png")
        plt.close()
    except Exception as e:
        print(f"Error drawing line chart: {e}")

    # CHART 3: BUBBLE CHART (STATIC PNG - LATEST YEAR)
    try:
        # Get latest year data
        max_year = df['Year'].max()
        latest_df = df[df['Year'] == max_year]
        
        plt.figure(figsize=(10, 6))
        # Bubble chart: x=MinWage, y=Unemployment, size=Schooling
        sns.scatterplot(data=latest_df, x='MinWage', y='Unemployment', 
                        size='Schooling', hue='CountryName', 
                        sizes=(50, 500), alpha=0.7, legend=False)
        
        # Add labels for some points to make it informative
        for i in range(latest_df.shape[0]):
             plt.text(latest_df.MinWage.iloc[i], latest_df.Unemployment.iloc[i], 
                      latest_df.CountryCode.iloc[i], fontsize=9, alpha=0.7)

        plt.title(f'Asian Economic Snapshot ({max_year})\n(Size = Schooling Years)')
        plt.xlabel('Minimum Wage (USD)')
        plt.ylabel('Unemployment Rate (%)')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig('chart_3_bubble_snapshot.png')
        print("Saved: chart_3_bubble_snapshot.png")
        plt.close()
    except Exception as e:
        print(f"Error drawing bubble chart: {e}")
        
    print("--- VISUALIZATION COMPLETE ---")

if __name__ == "__main__":
    visualize_data()

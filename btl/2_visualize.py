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

    # Define output directory
    output_dir = 'btl'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # CHART 1: CORRELATION HEATMAP
    try:
        plt.figure(figsize=(10, 8))
        corr = df[['Schooling', 'MinWage', 'Unemployment', 'MinWage_Growth', 'Unemployment_LastYear']].corr()
        sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f")
        plt.title('Correlation Matrix')
        save_path = os.path.join(output_dir, 'chart_1_correlation_heatmap.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
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
        save_path = os.path.join(output_dir, 'chart_2_trend_comparison.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
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
        save_path = os.path.join(output_dir, 'chart_3_bubble_snapshot.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
        plt.close()
    except Exception as e:
        print(f"Error drawing bubble chart: {e}")

    # CHART 4: BAR CHART - Schooling Comparison (Latest Year)
    try:
        max_year = df['Year'].max()
        latest_df = df[df['Year'] == max_year].sort_values('Schooling', ascending=False)
        
        plt.figure(figsize=(12, 8))
        sns.barplot(data=latest_df, x='Schooling', y='CountryName', palette='magma')
        plt.title(f'Mean Years of Schooling by Country ({max_year})')
        plt.xlabel('Years')
        plt.ylabel('Country')
        plt.tight_layout()
        save_path = os.path.join(output_dir, 'chart_4_bar_schooling.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
        plt.close()
    except Exception as e:
        print(f"Error drawing bar chart: {e}")

    # CHART 5: PIE CHART - Unemployment Classification (Latest Year)
    try:
        max_year = df['Year'].max()
        latest_df = df[df['Year'] == max_year].copy()
        
        def classify_unemployment(rate):
            if rate < 3: return 'Low (<3%)'
            elif rate <= 7: return 'Medium (3-7%)'
            else: return 'High (>7%)'
            
        latest_df['Category'] = latest_df['Unemployment'].apply(classify_unemployment)
        counts = latest_df['Category'].value_counts()
        
        plt.figure(figsize=(8, 8))
        plt.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=140, colors=['#66b3ff','#99ff99','#ff9999'])
        plt.title(f'Distribution of Countries by Unemployment Level ({max_year})')
        save_path = os.path.join(output_dir, 'chart_5_pie_unemployment.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
        plt.close()
    except Exception as e:
        print(f"Error drawing pie chart: {e}")

    # CHART 6: BOX PLOT - Unemployment Distribution Over Years
    try:
        plt.figure(figsize=(12, 6))
        sns.boxplot(data=df, x='Year', y='Unemployment', palette='Set3')
        plt.title('Distribution of Unemployment Rate (2015-2024)')
        plt.ylabel('Unemployment Rate (%)')
        plt.grid(True, axis='y', linestyle='--', alpha=0.5)
        save_path = os.path.join(output_dir, 'chart_6_box_unemployment.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
        plt.close()
    except Exception as e:
        print(f"Error drawing box plot: {e}")

    # CHART 7: SCATTER PLOT - Schooling vs Minimum Wage (All Years)
    try:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='Schooling', y='MinWage', hue='Year', palette='viridis', alpha=0.6)
        plt.title('Correlation: Education vs Minimum Wage (All Years)')
        plt.xlabel('Mean Years of Schooling')
        plt.ylabel('Minimum Wage (USD)')
        plt.grid(True, linestyle='--', alpha=0.5)
        save_path = os.path.join(output_dir, 'chart_7_scatter_schooling_wage.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
        plt.close()
    except Exception as e:
        print(f"Error drawing scatter plot: {e}")

    # CHART 8: REGRESSION PLOT (Last Year vs This Year)
    try:
        # Filter out rows where Unemployment_LastYear is 0 (first years)
        plot_df = df[df['Unemployment_LastYear'] > 0]
        
        plt.figure(figsize=(10, 6))
        sns.regplot(data=plot_df, x='Unemployment_LastYear', y='Unemployment', 
                    scatter_kws={'alpha':0.5, 'color':'teal'}, 
                    line_kws={'color':'red'})
        
        plt.title('Predictive Power: Unemployment (Last Year) vs (This Year)')
        plt.xlabel('Unemployment Rate Last Year (%)')
        plt.ylabel('Unemployment Rate This Year (%)')
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()
        save_path = os.path.join(output_dir, 'chart_8_lag_regression.png')
        plt.savefig(save_path)
        print(f"Saved: {save_path}")
        plt.close()
    except Exception as e:
        print(f"Error drawing regression plot: {e}")
        
    print("--- VISUALIZATION COMPLETE ---")

if __name__ == "__main__":
    visualize_data()

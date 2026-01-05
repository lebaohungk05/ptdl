import pandas as pd
import matplotlib
matplotlib.use('Agg') # Set backend to non-interactive
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import os

# Data path
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

    # CHART 2: INTERACTIVE TREND LINE
    try:
        top_countries = ['VNM', 'JPN', 'CHN', 'IND', 'THA']
        subset_df = df[df['CountryCode'].isin(top_countries)]
        
        fig_line = px.line(subset_df, x='Year', y='Unemployment', color='CountryName',
                      markers=True,
                      title='Unemployment Rate Comparison: Vietnam vs Asian Powers',
                      labels={'Unemployment': 'Unemployment Rate (%)'})
        
        fig_line.write_html("chart_2_trend_interactive.html")
        print("Saved: chart_2_trend_interactive.html")
    except Exception as e:
        print(f"Error drawing line chart: {e}")

    # CHART 3: BUBBLE CHART ANIMATION
    try:
        fig_bubble = px.scatter(df, x="MinWage", y="Unemployment",
                         animation_frame="Year", animation_group="CountryName",
                         size="Schooling", color="CountryName", 
                         hover_name="CountryName",
                         log_x=True, size_max=45, range_y=[0, 20],
                         title="Asian Economic Trends (2015-2024)")
        
        fig_bubble.write_html("chart_3_bubble_animation.html")
        print("Saved: chart_3_bubble_animation.html")
    except Exception as e:
        print(f"Error drawing bubble chart: {e}")
        
    print("--- VISUALIZATION COMPLETE ---")

if __name__ == "__main__":
    visualize_data()

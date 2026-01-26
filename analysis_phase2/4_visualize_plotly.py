import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import numpy as np
import os
from sklearn.linear_model import LinearRegression

# Setup
INPUT_FILE = 'cleaned_data.csv'
OUTPUT_DIR = 'charts_html'
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("--- Loading Data ---")
df = pd.read_csv(INPUT_FILE)
print(f"Loaded {df.shape[0]} rows.")

# ---------------------------------------------------------
# CHART 1: Correlation Heatmap (Ma trận tương quan)
# ---------------------------------------------------------
print("Generating Chart 1: Heatmap...")
numeric_df = df.select_dtypes(include=[np.number]).drop(columns=['Year'], errors='ignore')
corr = numeric_df.corr().round(2)

fig1 = px.imshow(corr,
                text_auto=True,
                aspect="auto",
                color_continuous_scale='RdBu_r',
                title="Chart 1: Correlation Matrix of Economic Indicators")
fig1.write_html(f"{OUTPUT_DIR}/chart_1_correlation.html")

# ---------------------------------------------------------
# CHART 2: Trend Comparison (So sánh xu hướng thất nghiệp)
# ---------------------------------------------------------
print("Generating Chart 2: Unemployment Trend...")
# Focus on some key economies to avoid clutter, or average vs specific
top_countries = ['Vietnam', 'China', 'Japan', 'India', 'Thailand', 'Indonesia']
df_filtered = df[df['Country Name'].isin(top_countries)]

fig2 = px.line(df_filtered, 
              x='Year', 
              y='Unemployment Rate', 
              color='Country Name',
              markers=True,
              title="Chart 2: Unemployment Rate Trends (Key Asian Economies)")
fig2.write_html(f"{OUTPUT_DIR}/chart_2_trend_comparison.html")

# ---------------------------------------------------------
# CHART 3: Bubble Snapshot (Biểu đồ bong bóng động)
# ---------------------------------------------------------
print("Generating Chart 3: Bubble Chart...")
# X: GDP per Capita (proxy via GDP/Pop growth? No, stick to raw GDP or Wage), Y: Unemployment, Size: Schooling
# Let's use Minimum Wage vs Unemployment
df_bubble = df.dropna(subset=['Minimum Wage (PPP)', 'Unemployment Rate', 'Mean Years of Schooling'])

fig3 = px.scatter(df_bubble, 
                 x="Minimum Wage (PPP)", 
                 y="Unemployment Rate", 
                 animation_frame="Year", 
                 animation_group="Country Name",
                 size="Mean Years of Schooling", 
                 color="Country Name", 
                 hover_name="Country Name",
                 log_x=True, 
                 size_max=45,
                 range_y=[0, 20],
                 title="Chart 3: Unemployment vs Wage vs Schooling (Motion Chart)")
fig3.write_html(f"{OUTPUT_DIR}/chart_3_bubble_motion.html")

# ---------------------------------------------------------
# CHART 4: Bar Chart (So sánh Học vấn)
# ---------------------------------------------------------
print("Generating Chart 4: Schooling Bar Chart...")
df_2023 = df[df['Year'] == 2023].sort_values('Mean Years of Schooling', ascending=True)

fig4 = px.bar(df_2023, 
             x='Mean Years of Schooling', 
             y='Country Name', 
             orientation='h',
             color='Mean Years of Schooling',
             title="Chart 4: Mean Years of Schooling (2023)")
fig4.update_layout(height=800) # Taller for many countries
fig4.write_html(f"{OUTPUT_DIR}/chart_4_bar_schooling.html")

# ---------------------------------------------------------
# CHART 5: Pie Chart (Cơ cấu GDP - Top 10)
# ---------------------------------------------------------
print("Generating Chart 5: GDP Pie Chart...")
df_2023_gdp = df[df['Year'] == 2023].sort_values('GDP (PPP)', ascending=False)
# Top 10 and "Others"
top_10 = df_2023_gdp.head(10)
others_gdp = df_2023_gdp.iloc[10:]['GDP (PPP)'].sum()
others_df = pd.DataFrame([{'Country Name': 'Others', 'GDP (PPP)': others_gdp}])
df_pie = pd.concat([top_10, others_df], ignore_index=True)

fig5 = px.pie(df_pie, 
             values='GDP (PPP)', 
             names='Country Name', 
             title="Chart 5: Share of GDP (PPP) in Asia (2023)")
fig5.write_html(f"{OUTPUT_DIR}/chart_5_pie_gdp.html")

# ---------------------------------------------------------
# CHART 6: Box Plot (Phân phối thất nghiệp)
# ---------------------------------------------------------
print("Generating Chart 6: Unemployment Box Plot...")
fig6 = px.box(df, 
             x='Year', 
             y='Unemployment Rate', 
             points="all",
             color='Year',
             title="Chart 6: Distribution of Unemployment Rate (2015-2024)")
fig6.write_html(f"{OUTPUT_DIR}/chart_6_box_unemployment.html")

# ---------------------------------------------------------
# CHART 7: Scatter Plot (Học vấn vs Lương)
# ---------------------------------------------------------
print("Generating Chart 7: Scatter Schooling vs Wage...")
fig7 = px.scatter(df, 
                 x='Mean Years of Schooling', 
                 y='Minimum Wage (PPP)', 
                 color='Country Name',
                 trendline="lowess", # Locally Weighted Scatterplot Smoothing
                 title="Chart 7: Relationship between Schooling and Minimum Wage")
fig7.write_html(f"{OUTPUT_DIR}/chart_7_scatter_schooling_wage.html")

# ---------------------------------------------------------
# CHART 8: Prediction vs Actual (Mô phỏng kết quả ML)
# ---------------------------------------------------------
print("Generating Chart 8: ML Prediction vs Actual...")
# Quickly rebuild the best model (Linear Regression) to generate points
df_model = df.copy()
df_model.sort_values(['Country Code', 'Year'], inplace=True)
df_model['Unemployment_Lag1'] = df_model.groupby('Country Code')['Unemployment Rate'].shift(1)
df_model.dropna(inplace=True)

X = df_model[['Mean Years of Schooling', 'Minimum Wage (PPP)', 'Unemployment_Lag1']] # Simplyfied features
y = df_model['Unemployment Rate']

model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

fig8 = px.scatter(x=y, y=y_pred, 
                 labels={'x': 'Actual Unemployment', 'y': 'Predicted Unemployment'},
                 title="Chart 8: Machine Learning Performance (Actual vs Predicted)")
# Add a diagonal line
fig8.add_shape(type="line", line=dict(dash='dash'),
              x0=y.min(), y0=y.min(), x1=y.max(), y1=y.max())

fig8.write_html(f"{OUTPUT_DIR}/chart_8_prediction_vs_actual.html")

print("--- All Charts Generated Successfully in 'analysis_phase2/charts_html' ---")

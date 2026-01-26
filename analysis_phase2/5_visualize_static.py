import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg') # Critical fix for headless/crashing environments
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.linear_model import LinearRegression

# Setup
INPUT_FILE = 'cleaned_data.csv'
OUTPUT_DIR = 'charts_png' # New folder for PNGs
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

print("--- Loading Data for PNG Generation ---")
df = pd.read_csv(INPUT_FILE)
sns.set_style("whitegrid")
sns.set_context("notebook", font_scale=1.0) # Scale for readability in reports

# ---------------------------------------------------------
# CHART 1: Correlation Heatmap
# ---------------------------------------------------------
print("Generating Chart 1: Heatmap...")
plt.figure(figsize=(12, 10))
numeric_df = df.select_dtypes(include=[np.number]).drop(columns=['Year'], errors='ignore')
corr = numeric_df.corr()
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, cmap='RdBu_r', fmt=".2f", square=True, linewidths=.5)
plt.title('Chart 1: Correlation Matrix of Economic Indicators')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_1_correlation_heatmap.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# CHART 2: Trend Comparison
# ---------------------------------------------------------
print("Generating Chart 2: Trend Comparison...")
plt.figure(figsize=(12, 6))
top_countries = ['Vietnam', 'China', 'Japan', 'India', 'Thailand', 'Indonesia']
df_filtered = df[df['Country Name'].isin(top_countries)]
sns.lineplot(data=df_filtered, x='Year', y='Unemployment Rate', hue='Country Name', marker='o', linewidth=2)
plt.title('Chart 2: Unemployment Trends - Key Asian Economies (2015-2024)')
plt.ylabel('Unemployment Rate (%)')
plt.grid(True, linestyle='--')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_2_trend_comparison.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# CHART 3: Bubble Chart Snapshot (Static version for 2023)
# ---------------------------------------------------------
print("Generating Chart 3: Bubble Chart (2023 Snapshot)...")
plt.figure(figsize=(12, 8))
df_2023 = df[df['Year'] == 2023].copy()
# Normalize size for display
size_factor = df_2023['Mean Years of Schooling'] * 20 

sns.scatterplot(data=df_2023, x='Minimum Wage (PPP)', y='Unemployment Rate', 
                size='Mean Years of Schooling', sizes=(50, 500), 
                hue='Country Name', legend=False, alpha=0.7)

# Annotate some countries
for i in range(df_2023.shape[0]):
    row = df_2023.iloc[i]
    if row['Minimum Wage (PPP)'] > 1000 or row['Unemployment Rate'] > 10:
        plt.text(row['Minimum Wage (PPP)'], row['Unemployment Rate'], 
                 row['Country Name'], fontsize=9, alpha=0.8)

plt.xscale('log')
plt.title('Chart 3: Wage vs Unemployment vs Schooling (2023 Snapshot)')
plt.xlabel('Minimum Wage (PPP) - Log Scale')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_3_bubble_snapshot.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# CHART 4: Bar Chart (Schooling)
# ---------------------------------------------------------
print("Generating Chart 4: Schooling Bar Chart...")
plt.figure(figsize=(10, 12)) # Tall chart
df_school = df[df['Year'] == 2023].sort_values('Mean Years of Schooling', ascending=False)
sns.barplot(data=df_school, x='Mean Years of Schooling', y='Country Name', palette='viridis')
plt.title('Chart 4: Average Years of Schooling by Country (2023)')
plt.xlabel('Years')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_4_bar_schooling.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# CHART 5: Pie Chart (Unemployment Structure - or GDP)
# ---------------------------------------------------------
print("Generating Chart 5: GDP Pie Chart...")
plt.figure(figsize=(10, 10))
df_gdp = df[df['Year'] == 2023].sort_values('GDP (PPP)', ascending=False)
top_8 = df_gdp.head(8)
others = pd.DataFrame([{'Country Name': 'Others', 'GDP (PPP)': df_gdp.iloc[8:]['GDP (PPP)'].sum()}])
df_pie = pd.concat([top_8, others], ignore_index=True)

plt.pie(df_pie['GDP (PPP)'], labels=df_pie['Country Name'], autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
plt.title('Chart 5: GDP (PPP) Distribution in Asia (2023)')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_5_pie_gdp.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# CHART 6: Box Plot
# ---------------------------------------------------------
print("Generating Chart 6: Box Plot...")
plt.figure(figsize=(12, 6))
sns.boxplot(data=df, x='Year', y='Unemployment Rate', palette="Set3")
plt.title('Chart 6: Distribution of Unemployment Rate Over Years')
plt.ylabel('Unemployment Rate (%)')
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_6_box_unemployment.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# CHART 7: Scatter Plot (Schooling vs Wage)
# ---------------------------------------------------------
print("Generating Chart 7: Scatter Schooling vs Wage...")
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='Mean Years of Schooling', y='Minimum Wage (PPP)', 
            scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
plt.title('Chart 7: Correlation between Schooling and Minimum Wage')
plt.ylim(0, 2000) # Limit y axis to see better (ignore outliers if any)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_7_scatter_schooling_wage.png", dpi=150)
plt.close()

# ---------------------------------------------------------
# CHART 8: ML Prediction
# ---------------------------------------------------------
print("Generating Chart 8: ML Actual vs Prediction...")
df_model = df.copy().sort_values(['Country Code', 'Year'])
df_model['Unemployment_Lag1'] = df_model.groupby('Country Code')['Unemployment Rate'].shift(1)
df_model.dropna(inplace=True)
X = df_model[['Mean Years of Schooling', 'Minimum Wage (PPP)', 'Unemployment_Lag1']]
y = df_model['Unemployment Rate']
model = LinearRegression()
model.fit(X, y)
y_pred = model.predict(X)

plt.figure(figsize=(8, 8))
plt.scatter(y, y_pred, alpha=0.6, color='blue')
plt.plot([y.min(), y.max()], [y.min(), y.max()], 'r--', lw=2) # Diagonal perfect fit line
plt.xlabel('Actual Unemployment Rate')
plt.ylabel('Predicted Unemployment Rate')
plt.title('Chart 8: Machine Learning Model Performance')
plt.grid(True)
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/chart_8_prediction_vs_actual.png", dpi=150)
plt.close()

print("--- All PNG Charts Generated Successfully in 'analysis_phase2/charts_png' ---")

import pandas as pd
import numpy as np

# Setup
INPUT_FILE = 'cleaned_data.csv'
OUTPUT_FILE = 'eda_report.txt'

def run_text_eda():
    df = pd.read_csv(INPUT_FILE)
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write("--- EXPLORATORY DATA ANALYSIS REPORT ---\\n\\n")
        
        # 1. Basic Stats
        f.write("1. BASIC STATISTICS\\n")
        f.write(df.describe().to_string())
        f.write("\\n\\n")
        
        # 2. Missing Values Check
        f.write("2. MISSING VALUES\\n")
        f.write(df.isnull().sum().to_string())
        f.write("\\n\\n")
        
        # 3. Correlation Matrix
        f.write("3. CORRELATION MATRIX\\n")
        numeric_df = df.select_dtypes(include=[np.number])
        corr = numeric_df.corr()
        f.write(corr.to_string())
        f.write("\\n\\n")
        
        # 4. Top 5 Countries by Unemployment (Avg)
        f.write("4. TOP 5 COUNTRIES - HIGHEST UNEMPLOYMENT (AVG)\\n")
        avg_unemp = df.groupby('Country Name')['Unemployment Rate'].mean().sort_values(ascending=False).head(5)
        f.write(avg_unemp.to_string())
        f.write("\\n\\n")
        
        # 5. Top 5 Countries by GDP (Avg)
        f.write("5. TOP 5 COUNTRIES - HIGHEST GDP (AVG)\\n")
        avg_gdp = df.groupby('Country Name')['GDP (PPP)'].mean().sort_values(ascending=False).head(5)
        f.write(avg_gdp.to_string())
        f.write("\\n\\n")

    print(f"EDA Report saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    run_text_eda()

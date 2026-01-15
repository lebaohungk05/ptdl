import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Đọc trực tiếp từ file gốc
input_path = r'data_ktl_group4.csv'

def visualize_raw():
    if not os.path.exists(input_path):
        print(f"Error: Not found {input_path}")
        return

    print("--- READING RAW DATA ---")
    # Đọc file, bỏ qua các cột trống lạ (như cột Unnamed)
    df = pd.read_csv(input_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Đổi tên cột cho gọn để dễ vẽ (nhưng vẫn giữ nguyên giá trị)
    df.columns = ['CountryCode', 'CountryName', 'Year', 'Schooling', 'MinWage', 'Unemployment']
    
    print("Columns:", df.columns.tolist())
    print(f"Total rows: {len(df)}")

    # 1. BIỂU ĐỒ CỘT: DỮ LIỆU BỊ THIẾU (MISSING VALUES)
    # Rất quan trọng để báo cáo: "Tại sao tôi phải điền dữ liệu khuyết?"
    try:
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0] # Chỉ lấy cột có thiếu
        
        if not missing_data.empty:
            plt.figure(figsize=(10, 6))
            sns.barplot(x=missing_data.index, y=missing_data.values, palette='Reds')
            plt.title('Missing Values Count in Raw Data')
            plt.ylabel('Number of Missing Rows')
            plt.grid(axis='y', linestyle='--')
            plt.savefig('raw_chart_1_missing_values.png')
            print("Saved: raw_chart_1_missing_values.png")
            plt.close()
        else:
            print("No missing values found to plot.")
    except Exception as e:
        print(f"Error drawing missing values: {e}")

    # 2. BIỂU ĐỒ TRÒN: TỈ TRỌNG THẤT NGHIỆP TRUNG BÌNH GIỮA CÁC NƯỚC
    # Xem nước nào chiếm "miếng bánh" thất nghiệp lớn nhất (xét về tỉ lệ %)
    try:
        avg_unemployment = df.groupby('CountryName')['Unemployment'].mean().sort_values(ascending=False)
        # Lấy top 10 nước cao nhất, còn lại gộp vào 'Others' cho gọn
        top_10 = avg_unemployment.head(10)
        others = pd.Series([avg_unemployment.iloc[10:].mean()], index=['Others (Avg)'])
        plot_data = pd.concat([top_10, others])

        plt.figure(figsize=(10, 10))
        # Fix: plt.pie doesn't support 'cmap' directly, generate colors first
        colors = sns.color_palette('tab20c', n_colors=len(plot_data))
        plt.pie(plot_data, labels=plot_data.index, autopct='%1.1f%%', startangle=140, colors=colors)
        plt.title('Average Unemployment Rate Share (Top 10 Countries)')
        plt.savefig('raw_chart_2_pie_avg_unemployment.png')
        print("Saved: raw_chart_2_pie_avg_unemployment.png")
        plt.close()
    except Exception as e:
        print(f"Error drawing pie chart: {e}")

    # 3. BIỂU ĐỒ CỘT NGANG: SO SÁNH LƯƠNG TỐI THIỂU TRUNG BÌNH (RAW)
    try:
        avg_wage = df.groupby('CountryName')['MinWage'].mean().sort_values(ascending=False)
        
        plt.figure(figsize=(12, 10))
        sns.barplot(x=avg_wage.values, y=avg_wage.index, palette='viridis')
        plt.title('Average Minimum Wage (2015-2024) - Raw Data')
        plt.xlabel('USD')
        plt.grid(axis='x', linestyle='--', alpha=0.5)
        plt.tight_layout()
        plt.savefig('raw_chart_3_bar_avg_wage.png')
        print("Saved: raw_chart_3_bar_avg_wage.png")
        plt.close()
    except Exception as e:
        print(f"Error drawing bar wage: {e}")

    # 4. BIỂU ĐỒ SCATTER: LƯƠNG vs THẤT NGHIỆP (RAW)
    # Để xem dữ liệu thô phân bố thế nào, có nhiễu (outliers) không
    try:
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x='MinWage', y='Unemployment', hue='Year', palette='deep', alpha=0.7)
        plt.title('Raw Scatter: Minimum Wage vs Unemployment')
        plt.xlabel('Minimum Wage (USD)')
        plt.ylabel('Unemployment Rate (%)')
        plt.grid(True, linestyle='--', alpha=0.3)
        plt.savefig('raw_chart_4_scatter_wage_unemployment.png')
        print("Saved: raw_chart_4_scatter_wage_unemployment.png")
        plt.close()
    except Exception as e:
        print(f"Error drawing scatter: {e}")
        
    # 5. BIỂU ĐỒ ĐƯỜNG: DIỄN BIẾN THẤT NGHIỆP CỦA VIỆT NAM VÀ CÁC NƯỚC KHÁC
    try:
        # Lọc một vài nước tiêu biểu để biểu đồ không bị rối
        countries = ['Vietnam', 'China', 'India', 'Indonesia', 'Thailand', 'Philippines']
        subset = df[df['CountryName'].isin(countries)]
        
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=subset, x='Year', y='Unemployment', hue='CountryName', marker='o')
        plt.title('Unemployment Trends (Selected Asian Countries) - Raw Data')
        plt.ylabel('Unemployment Rate (%)')
        plt.grid(True)
        plt.savefig('raw_chart_5_line_trends.png')
        print("Saved: raw_chart_5_line_trends.png")
        plt.close()
    except Exception as e:
        print(f"Error drawing line trends: {e}")

    print("--- RAW VISUALIZATION COMPLETE ---")

if __name__ == "__main__":
    visualize_raw()

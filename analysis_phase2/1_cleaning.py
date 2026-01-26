import pandas as pd
import numpy as np
import os

# --- Config ---
INPUT_FILE = '../data_ktl_group4 (1).csv'
OUTPUT_FILE = 'cleaned_data.csv'

def clean_data():
    print("--- Bắt đầu làm sạch dữ liệu ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv(INPUT_FILE)
        print(f"Đã đọc file: {INPUT_FILE} với kích thước {df.shape}")
    except FileNotFoundError:
        print(f"Lỗi: Không tìm thấy file {INPUT_FILE}")
        return

    # 2. Drop FDI column
    if 'FDI (USD)' in df.columns:
        df.drop(columns=['FDI (USD)'], inplace=True)
        print("Đã xóa cột 'FDI (USD)'")
    
    # 3. Handle Missing Values
    # Sắp xếp theo Quốc gia và Năm để nội suy chính xác
    df.sort_values(by=['Country Code', 'Year'], inplace=True)

    # Các cột cần xử lý số liệu (trừ các cột định danh)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    numeric_cols = [c for c in numeric_cols if c != 'Year'] # Không nội suy năm

    print("Đang xử lý dữ liệu thiếu...")
    
    # Chiến lược: 
    # - Nhóm theo Country Code
    # - Interpolate (linear) cho các giá trị ở giữa
    # - Forward Fill (ffill) cho các giá trị ở cuối (ví dụ năm 2024)
    # - Backward Fill (bfill) cho các giá trị ở đầu (nếu năm 2015 thiếu)
    
    for col in numeric_cols:
        # Interpolate
        df[col] = df.groupby('Country Code')[col].transform(lambda x: x.interpolate(method='linear', limit_direction='both'))
        
        # Fill remaining (specifically useful for 2024 if interpolate didn't catch it, though 'both' usually does)
        df[col] = df.groupby('Country Code')[col].transform(lambda x: x.ffill().bfill())

    # Special handling for Inflation Rate if it's still missing (whole countries missing)
    if df['Inflation Rate - CPI (%)'].isnull().sum() > 0:
        print("Phát hiện các quốc gia thiếu toàn bộ dữ liệu Lạm phát. Đang điền bằng trung bình năm (Yearly Mean)...")
        df['Inflation Rate - CPI (%)'] = df['Inflation Rate - CPI (%)'].fillna(df.groupby('Year')['Inflation Rate - CPI (%)'].transform('mean'))


    # Kiểm tra lại
    missing_sum = df.isnull().sum().sum()
    print(f"Tổng số giá trị thiếu sau khi xử lý: {missing_sum}")
    if missing_sum > 0:
        print(df.isnull().sum())

    # 4. Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Đã lưu dữ liệu sạch vào: {OUTPUT_FILE}")
    print("--- Hoàn thành bước làm sạch ---")

if __name__ == "__main__":
    clean_data()

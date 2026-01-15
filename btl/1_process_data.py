import pandas as pd
import numpy as np
import os

input_path = r'data_ktl_group4.csv'

output_path = r'final_dataset.csv'

def process_data():
    print("--- BẮT ĐẦU XỬ LÝ DỮ LIỆU ---")
    
    
    try:
        df = pd.read_csv(input_path)
        print(f"Đã đọc file: {input_path}")
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file tại {input_path}. Hãy kiểm tra lại.")
        return

   
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    
    df.columns = ['CountryCode', 'CountryName', 'Year', 'Schooling', 'MinWage', 'Unemployment']
    

    print("Đang xử lý dữ liệu thiếu...")
    
    numeric_cols = ['Schooling', 'MinWage', 'Unemployment']
    for col in numeric_cols:
        
        df[col] = df.groupby('CountryCode')[col].transform(lambda x: x.fillna(x.mean()))
    
    
    df = df.fillna(df.mean(numeric_only=True))

    
    print("Đang tạo biến đặc trưng mới (Feature Engineering)...")

   
    df = df.sort_values(by=['CountryCode', 'Year'])

    # Biến 1: Tăng trưởng lương (% Growth of MinWage)
    # Lương tăng bao nhiêu % so với năm ngoái?
    df['MinWage_Growth'] = df.groupby('CountryCode')['MinWage'].pct_change() * 100

    # Biến 2: Thất nghiệp năm trước (Lag Variable)
    # Logic: Thất nghiệp năm nay thường bị ảnh hưởng bởi năm ngoái
    df['Unemployment_LastYear'] = df.groupby('CountryCode')['Unemployment'].shift(1)

    
    df = df.fillna(0)

   
    df.to_csv(output_path, index=False)
    print(f"--- HOÀN TẤT: Dữ liệu sạch đã lưu tại '{output_path}' ---")
    print(df.head())

if __name__ == "__main__":
    process_data()

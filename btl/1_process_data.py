import pandas as pd
import numpy as np
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ---
# Đường dẫn file gốc (nằm ở thư mục cha)
input_path = r'../data_ktl_group4.csv'
# Đường dẫn file kết quả sẽ lưu
output_path = r'final_dataset.csv'

def process_data():
    print("--- BẮT ĐẦU XỬ LÝ DỮ LIỆU ---")
    
    # 1. Đọc dữ liệu
    # Dùng try-except để bắt lỗi nếu không tìm thấy file
    try:
        df = pd.read_csv(input_path)
        print(f"Đã đọc file: {input_path}")
    except FileNotFoundError:
        print(f"LỖI: Không tìm thấy file tại {input_path}. Hãy kiểm tra lại.")
        return

    # 2. Làm sạch cơ bản
    # Loại bỏ các cột "Unnamed" (cột rác do lỗi file CSV)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    # Đổi tên cột sang tiếng Anh chuẩn (dễ code, không dấu cách)
    df.columns = ['CountryCode', 'CountryName', 'Year', 'Schooling', 'MinWage', 'Unemployment']
    
    # 3. Xử lý Missing Values (Điền khuyết) - Kỹ thuật A+
    # Chiến thuật: Điền bằng giá trị trung bình CỦA CHÍNH QUỐC GIA ĐÓ.
    # Nếu quốc gia đó không có dữ liệu nào -> Điền bằng trung bình toàn Châu Á.
    print("Đang xử lý dữ liệu thiếu...")
    
    numeric_cols = ['Schooling', 'MinWage', 'Unemployment']
    for col in numeric_cols:
        # Nhóm theo quốc gia và điền mean
        df[col] = df.groupby('CountryCode')[col].transform(lambda x: x.fillna(x.mean()))
    
    # Điền nốt những ô vẫn còn thiếu (do cả quốc gia đó không có dữ liệu)
    df = df.fillna(df.mean(numeric_only=True))

    # 4. Feature Engineering (Tạo biến mới) - PHẦN ĂN ĐIỂM SÁNG TẠO
    print("Đang tạo biến đặc trưng mới (Feature Engineering)...")

    # Sắp xếp lại để tính toán theo thời gian đúng
    df = df.sort_values(by=['CountryCode', 'Year'])

    # Biến 1: Tăng trưởng lương (% Growth of MinWage)
    # Lương tăng bao nhiêu % so với năm ngoái?
    df['MinWage_Growth'] = df.groupby('CountryCode')['MinWage'].pct_change() * 100

    # Biến 2: Thất nghiệp năm trước (Lag Variable)
    # Logic: Thất nghiệp năm nay thường bị ảnh hưởng bởi năm ngoái
    df['Unemployment_LastYear'] = df.groupby('CountryCode')['Unemployment'].shift(1)

    # Sau khi tạo biến trễ (lag), dòng đầu tiên của mỗi nước sẽ bị NaN -> Ta điền bằng 0 hoặc backfill
    df = df.fillna(0)

    # 5. Lưu kết quả
    df.to_csv(output_path, index=False)
    print(f"--- HOÀN TẤT: Dữ liệu sạch đã lưu tại '{output_path}' ---")
    print(df.head())

if __name__ == "__main__":
    process_data()

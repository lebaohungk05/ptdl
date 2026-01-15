# BÁO CÁO TỔNG KẾT DỰ ÁN PHÂN TÍCH DỮ LIỆU (NHÓM 4)

Dự án thực hiện phân tích mối liên hệ giữa Giáo dục, Lương tối thiểu và Tỷ lệ thất nghiệp tại các quốc gia Châu Á (2015-2024).

---

## 1. Thu thập dữ liệu
- **Nguồn:** Dữ liệu kinh tế - xã hội tổng hợp.
- **Tập dữ liệu:** `data_ktl_group4.csv`
- **Các biến chính:**
    - `Country Code/Name`: Danh tính quốc gia.
    - `Year`: Thời gian (2015 - 2024).
    - `Mean Years of Schooling`: Trình độ học vấn (số năm đi học bình quân).
    - `Minimum Wage`: Mức lương tối thiểu (USD).
    - `Unemployment Rate`: Tỷ lệ thất nghiệp (%).

## 2. Làm sạch dữ liệu (Data Cleaning)
*Thực hiện tại: `btl/1_process_data.py`*
- **Chuẩn hóa:** Đổi tên các cột về dạng ngắn gọn, dễ lập trình.
- **Xử lý dữ liệu thiếu (Imputation):**
    - Ưu tiên điền giá trị thiếu bằng trung bình của chính quốc gia đó qua các năm.
    - Điền các giá trị còn lại bằng trung bình chung của toàn bộ tập dữ liệu.
- **Định dạng:** Đảm bảo kiểu dữ liệu số cho các cột tính toán.

## 3. Khai phá và trực quan hóa (EDA)
*Thực hiện tại: `btl/1_process_data.py` & `btl/2_visualize.py`*
- **Kỹ thuật đặc trưng (Feature Engineering):**
    - Tạo biến `MinWage_Growth`: Phần trăm tăng trưởng lương hàng năm.
    - Tạo biến `Unemployment_LastYear`: Độ trễ của tỷ lệ thất nghiệp (biến quan trọng nhất để dự báo).
- **Trực quan hóa tiêu biểu:**
    - **Heatmap:** Kiểm tra tương quan giữa Giáo dục và Lương.
    - **Trend Chart:** So sánh tỷ lệ thất nghiệp của Việt Nam với các nước lớn (Nhật Bản, Trung Quốc...).
    - **Boxplot:** Phân tích sự biến động của thị trường lao động qua từng năm.

## 4. Lập mô hình học máy (Machine Learning)
*Thực hiện tại: `btl/3_machine_learning.py`*
- **Bài toán 1 (Hồi quy):** Dự đoán tỷ lệ thất nghiệp.
    - Sử dụng: `Linear Regression`, `Random Forest`, `Gradient Boosting`.
- **Bài toán 2 (Phân cụm):** Nhóm các quốc gia có đặc điểm kinh tế tương đồng.
    - Sử dụng: `K-Means Clustering` (3 cụm).

## 5. Lựa chọn đặc trưng (Feature Selection)
- **Phương pháp:** Sử dụng thuộc tính `feature_importances_` từ mô hình Random Forest.
- **Kết quả:**
    1. `Unemployment_LastYear`: 91.5% (Ảnh hưởng lớn nhất).
    2. `Schooling`: 5.1%.
    3. `MinWage`: 2.9%.
    4. `MinWage_Growth`: 0.5%.

## 6. Đánh giá và so sánh mô hình
*Dựa trên kết quả tại `ml_report.txt`*

| Mô hình | RMSE (Sai số) | R2 Score (Độ chính xác) |
| :--- | :--- | :--- |
| Linear Regression | 2.0353 | 0.7990 |
| Random Forest | 1.7259 | 0.8555 |
| **Gradient Boosting** | **1.5102** | **0.8893** |

- **Kết luận:** Mô hình Gradient Boosting cho kết quả tối ưu nhất với độ chính xác ~89%.

## 7. Kết luận và Truyền đạt
- **Hiểu biết sâu sắc:** Tỷ lệ thất nghiệp của một năm chịu ảnh hưởng cực lớn bởi năm trước đó. Trình độ giáo dục có tương quan tỷ lệ thuận với mức lương tối thiểu.
- **Sản phẩm đầu ra:** 
    - Bộ code xử lý dữ liệu tự động.
    - Hệ thống 8 biểu đồ phân tích chuyên sâu.
    - File dữ liệu đã phân cụm: `final_dataset_with_clusters.csv`.

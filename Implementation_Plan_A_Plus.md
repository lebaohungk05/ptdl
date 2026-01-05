# IMPLEMENTATION PLAN & BÁO CÁO THỰC HIỆN DỰ ÁN (FINAL)

## 1. Tổng quan Dự án
*   **Tên đề tài:** Phân tích và Dự báo Tỷ lệ thất nghiệp Châu Á sử dụng Machine Learning.
*   **Mục tiêu:** Vượt qua các phân tích thống kê cơ bản (như OLS trong Kinh tế lượng) bằng cách áp dụng các thuật toán Học máy hiện đại để dự báo chính xác hơn và tìm ra các mẫu hình ẩn (patterns).
*   **Công cụ thực hiện:** Python 3.12, Pandas, Seaborn, Plotly (Tương tác), Scikit-learn.

---

## 2. Chi tiết Triển khai (Đã hoàn tất)

### Giai đoạn 1: Xử lý dữ liệu & Feature Engineering
**File code:** `1_process_data.py`

*   **Làm sạch dữ liệu (Data Cleaning):**
    *   Xử lý lỗi định dạng CSV (cột rác `Unnamed`).
    *   **Điền khuyết (Imputation):** Thay vì xóa dữ liệu, đã sử dụng kỹ thuật điền giá trị trung bình theo từng quốc gia (Group Mean Imputation) để giữ lại tối đa thông tin.
*   **Kỹ thuật Feature Engineering (Tạo biến mới) - *Điểm nhấn A+*:**
    *   Tạo biến `MinWage_Growth`: Tốc độ tăng trưởng lương tối thiểu (%) -> Giúp mô hình bắt được xu hướng thay đổi chính sách.
    *   Tạo biến `Unemployment_LastYear`: Biến trễ (Lag feature) -> Giúp mô hình học được tính "quán tính" của nền kinh tế.

### Giai đoạn 2: Trực quan hóa dữ liệu (EDA)
**File code:** `2_visualize.py`

*   **Biểu đồ tĩnh (Static):**
    *   *Ma trận tương quan (Heatmap):* Chỉ ra mối quan hệ giữa các biến số.
*   **Biểu đồ tương tác (Interactive) - *Yêu cầu cao cấp*:**
    *   *Line Chart (Plotly):* So sánh xu hướng thất nghiệp của 5 cường quốc (VN, Nhật, Trung, Ấn, Thái) với khả năng zoom/pan.
    *   *Animated Bubble Chart:* Biểu diễn 4 chiều dữ liệu (X: Lương, Y: Thất nghiệp, Size: Học vấn, Time: Năm) chuyển động theo thời gian.

### Giai đoạn 3: Học máy & Tối ưu hóa (Machine Learning)
**File code:** `3_machine_learning.py`

#### Bài toán 1: Dự báo Tỷ lệ thất nghiệp (Regression)
Đã xây dựng và so sánh 3 mô hình (đáp ứng yêu cầu tối thiểu 3 mô hình của giảng viên):
1.  **Linear Regression:** Mô hình cơ sở (Baseline).
2.  **Random Forest Regressor:** Mô hình phi tuyến tính mạnh mẽ.
3.  **Gradient Boosting Regressor:** Mô hình tối ưu (thường dùng trong thi đấu Data Science).

**Kết quả thực nghiệm:**
*   Gradient Boosting đạt hiệu suất tốt nhất với **$R^2 \approx 89\%$** và **RMSE $\approx$ 1.51**.
*   Vượt trội hoàn toàn so với phân tích OLS truyền thống ($R^2$ thường thấp).

**Tối ưu hóa (Optimization):**
*   Sử dụng **GridSearchCV** để tinh chỉnh tham số (Hyperparameter Tuning) cho Random Forest.
*   **Feature Importance:** Xác định biến `Unemployment_LastYear` (Thất nghiệp năm trước) là yếu tố dự báo quan trọng nhất (chiếm >90% trọng số).

#### Bài toán 2: Phân cụm Quốc gia (Clustering)
*   Sử dụng thuật toán **K-Means**.
*   Phân chia các quốc gia Châu Á thành 3 nhóm đặc thù dựa trên đặc điểm Lương và Học vấn.
*   Kết quả được trực quan hóa rõ ràng trên biểu đồ Scatter Plot.

---

## 3. Đáp ứng yêu cầu Giảng viên (Checklist)

| Yêu cầu (trong sos.md) | Trạng thái | Minh chứng trong dự án |
| :--- | :--- | :--- |
| 1. Thu thập dữ liệu | ✅ Hoàn thành | Dữ liệu World Bank/ILO (final_dataset.csv) |
| 2. Làm sạch dữ liệu | ✅ Hoàn thành | Code `1_process_data.py` (Imputation, Cleaning) |
| 3. Khai phá & Phân tích | ✅ Hoàn thành | Code `2_visualize.py` (Heatmap, Interactive Charts) |
| 4. Lập mô hình học máy | ✅ Hoàn thành | Regression (Dự báo) & Clustering (Phân cụm) |
| 5. Lựa chọn Features, Tối ưu | ✅ Hoàn thành | GridSearch, Feature Importance Analysis, RFE |
| 6. Đánh giá & So sánh | ✅ Hoàn thành | So sánh RMSE, R2 của 3 mô hình (Linear, RF, GBoost) |
| 7. Truyền đạt kết quả | ✅ Hoàn thành | Xuất ra HTML, PNG và CSV kết quả |

---

## 4. Hướng dẫn chạy lại dự án
Mở Terminal tại thư mục `D:\ptdl\btl` và chạy lần lượt:

1.  `python 1_process_data.py` -> Tạo dữ liệu sạch.
2.  `python 2_visualize.py` -> Vẽ biểu đồ.
3.  `python 3_machine_learning.py` -> Chạy mô hình và xuất kết quả.

---
*Plan updated: 03/01/2026*
# KẾ HOẠCH HỌC TẬP & BẢO VỆ DỰ ÁN (LEARNING PLAN)

Tài liệu này giúp bạn nắm vững toàn bộ dự án từ A-Z để tự tin trình bày và phản biện trước giảng viên.

---

## 📅 LỘ TRÌNH TỔNG QUAN
Dự án đi theo luồng dữ liệu (Data Pipeline):
1.  **Bước 1: `1_process_data.py`** - Chuẩn bị "nguyên liệu" (Xử lý dữ liệu).
2.  **Bước 2: `2_visualize.py`** - Kể chuyện dữ liệu (Trực quan hóa).
3.  **Bước 3: `3_machine_learning.py`** - Xây dựng "trí tuệ" (Mô hình dự báo & Phân cụm).
4.  **Bước 4: Tổng kết** - Kết quả cuối cùng & Bài học.

---

## 🛠️ CHI TIẾT TỪNG PHẦN

### BƯỚC 1: XỬ LÝ DỮ LIỆU (`1_process_data.py`)

#### 💡 Ý tưởng cốt lõi
Biến dữ liệu thô (nhiều lỗi, thiếu) thành dữ liệu sạch, giàu ý nghĩa.

#### 🔑 Các kỹ thuật quan trọng (Key Points)
1.  **Imputation (Điền khuyết):** 
    *   *Cách làm:* Thay vì xóa dòng thiếu (mất dữ liệu), ta điền bằng **Giá trị trung bình của chính quốc gia đó**.
    *   *Tại sao:* Giữ được đặc trưng riêng của từng nước (VD: Không lấy lương của Nhật điền cho Việt Nam).
2.  **Feature Engineering (Tạo biến mới) - *Điểm A+*:**
    *   `MinWage_Growth`: Tốc độ tăng trưởng lương (%). Đo lường sự thay đổi chính sách.
    *   `Unemployment_LastYear`: Tỷ lệ thất nghiệp năm ngoái. Giúp mô hình học được tính "quán tính" (năm nay thường ảnh hưởng bởi năm ngoái).

#### 🗣️ Q&A (Giảng viên hỏi - Mình trả lời)
*   **Hỏi:** Tại sao em tạo thêm cột năm trước (`LastYear`)?
*   **Đáp:** Dạ, vì trong kinh tế, thất nghiệp có tính chu kỳ và quán tính. Dữ liệu quá khứ gần nhất là chỉ báo tốt nhất cho hiện tại ạ.

---

### BƯỚC 2: TRỰC QUAN HÓA (`2_visualize.py`)

#### 💡 Ý tưởng cốt lõi
Dùng hình ảnh để chứng minh sự hiểu biết về dữ liệu trước khi chạy mô hình.

#### 🔑 Các loại biểu đồ
1.  **Heatmap (Bản đồ nhiệt):** Xem tương quan.
    *   *Insight:* Lương tối thiểu và Thất nghiệp có tương quan dương/âm như thế nào?
2.  **Interactive Bubble Chart (Biểu đồ bong bóng động):**
    *   Biểu diễn 4 chiều: Trục X (Lương), Trục Y (Thất nghiệp), Kích thước bóng (Học vấn), Thời gian (Chạy theo năm).
    *   *Tác dụng:* Cho thấy sự dịch chuyển của các nền kinh tế qua từng năm (VD: Trung Quốc bóng to dần và di chuyển nhanh).

#### 🗣️ Q&A
*   **Hỏi:** Biểu đồ bong bóng cho thấy điều gì nổi bật?
*   **Đáp:** Dạ, nó cho thấy các nước phát triển (bóng to, học vấn cao) thường tụ về một nhóm có mức lương cao ổn định, trong khi các nước đang phát triển biến động thất nghiệp rất mạnh.

---

### BƯỚC 3: MÁY HỌC & DỰ BÁO (`3_machine_learning.py`)

#### 💡 Ý tưởng cốt lõi
Giải quyết 2 bài toán lớn: **Dự báo (Regression)** và **Phân nhóm (Clustering)**.

#### 🔑 Bài toán 1: Dự báo Thất nghiệp (Regression)
Em dùng 3 mô hình để so sánh:
1.  **Linear Regression:** Đơn giản, dùng làm mốc so sánh (Baseline).
2.  **Random Forest:** Mạnh mẽ, bắt được quan hệ phi tuyến tính.
3.  **Gradient Boosting:** *Mô hình tốt nhất (Best Model)*.
    *   **Kết quả:** $R^2 \approx 89\%$ (Giải thích được 89% sự biến động của dữ liệu).
    *   **RMSE:** Sai số thấp nhất.

#### 🔑 Bài toán 2: Phân cụm (Clustering)
*   Thuật toán: **K-Means**.
*   Kết quả: Chia Châu Á thành 3 nhóm (Cluster 0, 1, 2).
    *   Nhóm 0: Phát triển (Lương cao, Học vấn cao).
    *   Nhóm 1: Đang phát triển.
    *   Nhóm 2: Nhóm mới nổi/Thấp hơn.

#### 🗣️ Q&A
*   **Hỏi:** Tại sao Gradient Boosting tốt hơn Linear Regression?
*   **Đáp:** Dạ, vì Linear chỉ vẽ được đường thẳng, còn kinh tế thực tế rất phức tạp (phi tuyến). Gradient Boosting học từ sai số của các cây quyết định trước đó nên tối ưu tốt hơn nhiều ạ.
*   **Hỏi:** Em đánh giá mô hình bằng chỉ số nào?
*   **Đáp:** Em dùng $R^2$ (độ phù hợp) và RMSE (sai số trung bình phương).

---

## 🎓 TỔNG KẾT (Dùng để chốt bài)
"Dự án của em không chỉ dừng lại ở phân tích thống kê mà đã ứng dụng thành công Machine Learning để dự báo với độ chính xác ~89%. Việc phân cụm cũng giúp gợi ý các nhóm chính sách kinh tế phù hợp cho từng nhóm quốc gia."

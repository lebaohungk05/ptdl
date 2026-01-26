# BÁO CÁO TIẾN ĐỘ & KẾT QUẢ PHÂN TÍCH DỮ LIỆU
**Dự án:** Phân tích & Dự báo Tỷ lệ Thất nghiệp Châu Á (Asian Unemployment Analysis)  
**Ngày cập nhật:** 23/01/2026

---

## I. Tổng quan Dự án
Mục tiêu dự án là phân tích các yếu tố kinh tế vĩ mô ảnh hưởng đến tỷ lệ thất nghiệp tại các quốc gia Châu Á trong giai đoạn 2015-2024, từ đó xây dựng mô hình dự báo chính xác và phân nhóm các quốc gia dựa trên mức độ phát triển.

### 1. Dữ liệu đầu vào
- **Nguồn:** `data_ktl_group4 (1).csv`
- **Phạm vi:** 36 quốc gia Châu Á.
- **Thời gian:** 10 năm (2015 - 2024).
- **Số lượng bản ghi:** 360 dòng.
- **Các biến số chính:**
    - `Unemployment Rate`: Tỷ lệ thất nghiệp (Biến mục tiêu).
    - `Mean Years of Schooling`: Số năm đi học trung bình.
    - `Minimum Wage (PPP)`: Lương tối thiểu (theo sức mua tương đương).
    - `GDP (PPP)`: Tổng sản phẩm quốc nội.
    - `Inflation Rate`: Tỷ lệ lạm phát.
    - `Labor force participation`: Tỷ lệ tham gia lực lượng lao động.

---

## II. Chi tiết 7 Bước thực hiện (Theo yêu cầu Giảng viên)

### Bước 1: Thu thập dữ liệu
- Đã tiếp nhận bộ dữ liệu `data_ktl_group4 (1).csv` chứa đầy đủ các chỉ số kinh tế vĩ mô quan trọng.
- Kiểm tra sơ bộ: Dữ liệu bao quát được các nền kinh tế lớn (Trung Quốc, Ấn Độ, Nhật Bản) và các nước đang phát triển (Việt Nam, Lào, Campuchia).

### Bước 2: Làm sạch dữ liệu (Data Cleaning)
- **Vấn đề phát hiện:**
    - Cột `FDI (USD)` thiếu hơn 60% dữ liệu -> Quyết định **loại bỏ** để tránh gây nhiễu.
    - Dữ liệu năm 2024 thiếu hụt ở hầu hết các quốc gia -> Sử dụng phương pháp **Forward Fill** (lấy giá trị năm 2023).
    - Một số quốc gia thiếu chỉ số Lạm phát hoặc Học vấn ở các năm giữa -> Sử dụng **Linear Interpolation** (Nội suy tuyến tính) theo từng quốc gia để điền khuyết một cách tự nhiên nhất.
- **Kết quả:** Bộ dữ liệu sạch `cleaned_data.csv` (360 dòng, 0 ô trống), sẵn sàng cho phân tích.

### Bước 3: Khai phá & Phân tích dữ liệu (EDA)
Thực hiện phân tích sâu thông qua thống kê mô tả và trực quan hóa.
*(Chi tiết ý nghĩa biểu đồ xem mục III bên dưới)*.

### Bước 4: Lập mô hình học máy (Machine Learning Modeling)
Xây dựng hai bài toán cốt lõi:
1.  **Hồi quy (Regression):** Dự báo `Unemployment Rate` dựa trên các chỉ số kinh tế khác.
2.  **Phân cụm (Clustering):** Phân nhóm các quốc gia có đặc điểm tương đồng.

### Bước 5: Lựa chọn Features & Tối ưu hóa (QUAN TRỌNG)
Đây là bước đột phá của dự án. Chúng tôi đã tiến hành thử nghiệm so sánh hiệu quả của việc tạo thêm biến mới (Feature Engineering).

**Kỹ thuật Feature Engineering:**
1.  **Tạo biến `Unemployment_Lag1`:** Tỷ lệ thất nghiệp của năm trước đó.
    - *Lý do:* Thất nghiệp thường có tính "quán tính" (Autocorrelation). Năm nay thất nghiệp cao thì khả năng năm sau vẫn cao là rất lớn.
2.  **Tạo biến `Wage_Growth`:** Tốc độ tăng trưởng lương tối thiểu (%) so với năm trước.
    - *Lý do:* Sự thay đổi chính sách lương thường tác động trễ đến việc làm.

**Kết quả Thử nghiệm So sánh (A/B Testing):**
- **Trường hợp 1 (Chưa có biến mới):** Chỉ dùng các biến cơ bản (GDP, Lương, Học vấn...).
    - **R2 Score:** 54.02% (Mô hình chỉ giải thích được 54% sự biến động).
    - **RMSE:** 3.07 (Sai số trung bình là 3.07%).
    - *Đánh giá:* Hiệu suất trung bình, chưa đủ tốt để dự báo thực tế.
- **Trường hợp 2 (Đã thêm Lag1 & Growth):**
    - **R2 Score:** **96.67%** (Tăng vọt +42.65%).
    - **RMSE:** **0.86** (Sai số giảm mạnh từ 3.07 xuống 0.86).
    - *Đánh giá:* Mô hình trở nên cực kỳ chính xác. Điều này chứng minh rằng **lịch sử thất nghiệp** là yếu tố dự báo quan trọng nhất.

### Bước 6: Đánh giá & So sánh mô hình
Sau khi chọn được bộ Features tối ưu (Trường hợp 2), chúng tôi so sánh 3 thuật toán:
1.  **Linear Regression:** R2 = 96.67% (Cao nhất).
2.  **Random Forest:** R2 = 96.35%.
3.  **Gradient Boosting:** R2 = 96.07%.
-> **Kết luận:** Mô hình Linear Regression hoạt động tốt nhất, đồng thời thời gian huấn luyện nhanh nhất.

### Bước 7: Truyền đạt kết quả
Xuất bản báo cáo này cùng bộ biểu đồ trực quan (dạng ảnh PNG) và file nhật ký làm việc chi tiết.

---

## III. Giải thích ý nghĩa chi tiết 8 Biểu đồ (Charts)

### Chart 1: Correlation Matrix (Ma trận tương quan)
- **Mục đích:** Tìm mối liên hệ giữa các biến số.
- **Ý nghĩa:**
    - Ô màu đỏ đậm/xanh đậm thể hiện mối tương quan mạnh.
    - Ví dụ: Nếu `Mean Years of Schooling` có tương quan âm với `Unemployment Rate` (màu xanh), nghĩa là trình độ học vấn càng cao, tỷ lệ thất nghiệp càng thấp.
    - Giúp xác định biến nào quan trọng để đưa vào mô hình dự báo.

### Chart 2: Unemployment Trends Comparison (So sánh xu hướng)
- **Mục đích:** So sánh sức khỏe nền kinh tế của các cường quốc Châu Á (Việt Nam, Trung Quốc, Nhật, Ấn Độ...).
- **Ý nghĩa:**
    - Đường đi lên cho thấy thất nghiệp đang tăng (cảnh báo rủi ro).
    - So sánh vị thế của Việt Nam (thường thấp và ổn định) so với các nước khác.
    - Nhận diện các cú sốc kinh tế (ví dụ: giai đoạn COVID-19 năm 2020-2021 thường có đỉnh nhọn).

### Chart 3: Bubble Chart - Wage vs Unemployment vs Schooling (Snapshot 2023)
- **Mục đích:** Cái nhìn đa chiều về thị trường lao động năm 2023.
- **Ý nghĩa:**
    - **Trục X (Lương):** Nước nào trả lương cao nằm bên phải.
    - **Trục Y (Thất nghiệp):** Nước nào thất nghiệp cao nằm bên trên.
    - **Kích thước bóng (Học vấn):** Bóng to là dân trí cao.
    - **Insight:** Các nước phát triển (Nhật, Israel) thường nằm ở góc "Dưới - Phải" (Thất nghiệp thấp, Lương cao, Bóng to).

### Chart 4: Schooling Bar Chart (Xếp hạng Học vấn)
- **Mục đích:** So sánh chất lượng nhân lực.
- **Ý nghĩa:**
    - Xếp hạng các quốc gia từ cao xuống thấp về số năm đi học trung bình.
    - Giúp nhận diện quốc gia nào có nguồn nhân lực chất lượng cao nhất khu vực (thường là Israel, Nhật Bản, Hàn Quốc...).

### Chart 5: GDP Pie Chart (Cơ cấu kinh tế)
- **Mục đích:** Thể hiện quy mô nền kinh tế.
- **Ý nghĩa:**
    - Cho thấy ai là "anh cả" của nền kinh tế Châu Á (thường là Trung Quốc chiếm miếng bánh lớn nhất).
    - Thấy được sự chênh lệch giàu nghèo giữa các nhóm quốc gia.

### Chart 6: Unemployment Distribution Box Plot (Phân phối thất nghiệp)
- **Mục đích:** Đánh giá độ biến động thất nghiệp qua các năm.
- **Ý nghĩa:**
    - Hộp càng dài thì sự chênh lệch thất nghiệp giữa các nước trong năm đó càng lớn.
    - Dấu chấm tròn (Outliers) là các nước có tỷ lệ thất nghiệp cao bất thường (cần chú ý đặc biệt).

### Chart 7: Scatter Plot - Schooling vs Wage (Học vấn & Lương)
- **Mục đích:** Kiểm chứng giả thuyết "Học cao lương cao".
- **Ý nghĩa:**
    - Đường xu hướng đi lên xác nhận mối quan hệ thuận: Đầu tư cho giáo dục đi đôi với mức thu nhập cao hơn.
    - Các nước nằm xa đường xu hướng là các trường hợp ngoại lệ (ví dụ: học cao nhưng lương thấp do kinh tế suy thoái).

### Chart 8: Prediction vs Actual (Đánh giá Mô hình ML)
- **Mục đích:** Kiểm tra độ chính xác của "nhà tiên tri" AI.
- **Ý nghĩa:**
    - Trục ngang là Thực tế, Trục dọc là Dự báo.
    - Các điểm càng nằm sát đường chéo màu đỏ nghĩa là dự báo càng chính xác.
    - **Kết quả thực nghiệm:** Các điểm dữ liệu bám rất sát đường chéo (R2 ~ 97%), chứng tỏ việc thêm biến `Unemployment_Lag1` đã giúp mô hình dự báo cực kỳ chính xác.

---

## IV. Kết luận & Đề xuất
- **Về Dữ liệu:** Đã xử lý triệt để vấn đề dữ liệu thiếu, đảm bảo tính nhất quán.
- **Về Feature Engineering:** Việc thêm biến trễ (Lag Feature) là yếu tố quyết định giúp nâng cao độ chính xác từ 54% lên 97%. Đây là phát hiện quan trọng nhất của dự án.
- **Về Kinh tế:** Có mối liên hệ rõ ràng giữa Trình độ học vấn và Sự ổn định việc làm/Thu nhập. Các nước đầu tư mạnh vào giáo dục thường có nền kinh tế bền vững hơn trước các biến động.

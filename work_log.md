CHƯƠNG 1: MỞ ĐẦU
  1.1. Bối cảnh nghiên cứu (Tầm quan trọng của chỉ số thất nghiệp đối với kinh tế Châu Á).
  1.2. Mục tiêu nghiên cứu (Tìm yếu tố ảnh hưởng mạnh nhất & Xây dựng mô hình dự báo chính xác cao).
  1.3. Đối tượng và phạm vi (Một số quốc gia Châu Á, giai đoạn 2015-2024).


  CHƯƠNG 2: DỮ LIỆU VÀ PHƯƠNG PHÁP NGHIÊN CỨU
  2.1. Nguồn dữ liệu (World Bank, ILOSTAT, UNDP) và mô tả các biến (12 biến độc lập).
  2.2. Quy trình tiền xử lý dữ liệu:
      - Xử lý giá trị thiếu (Bỏ cột FDI, dùng Linear Interpolation, Ffill/Bfill).
      - Làm giàu dữ liệu (Enrichment): So sánh tham số và thuộc tính giữa các quốc gia.
  2.3. Kỹ thuật đặc trưng (Feature Engineering):
      - Cách tạo biến Unemployment_Lag1 (Biến trễ).
      - Cách tạo biến Wage_Growth (Tăng trưởng lương).


  CHƯƠNG 3: PHÂN TÍCH KHÁM PHÁ DỮ LIỆU (EDA) VÀ ĐÁNH GIÁ THỰC TẾ
  3.1. Thống kê mô tả và trực quan hóa phân phối (GDP, Lạm phát, Thất nghiệp).
  3.2. Phân tích tương quan giữa các đặc trưng (Ma trận tương quan).
  3.3. Giải thích ý nghĩa thực tế :
      - Tại sao tỷ lệ tham gia lực lượng lao động (Labor force participation) lại ảnh hưởng mạnh nhất đến thất nghiệp?
      - Mối quan hệ giữa trình độ học vấn (Schooling) và mức lương tối thiểu đối với thất nghiệp tại các nước Châu Á.


  CHƯƠNG 4: TỐI ƯU HÓA VÀ XÂY DỰNG MÔ HÌNH DỰ BÁO
  4.1. Kỹ thuật giảm chiều dữ liệu :
      - Áp dụng PCA (Principal Component Analysis) hoặc Feature Selection để loại bỏ dữ liệu dư thừa.
      - So sánh hiệu quả mô hình trước và sau khi giảm chiều.
  4.2. Quy trình huấn luyện 3 giai đoạn:
      - Giai đoạn 1: Baseline Model (Sử dụng biến gốc).
      - Giai đoạn 2: Model với Feature Engineering (Biến Lag1, Wage Growth).
  4.3. Đánh giá và So sánh các mô hình (Linear Regression, Random Forest, Gradient Boosting).
      - Tại sao Linear Regression lại đạt độ chính xác cao nhất (R2 = 0.9667)?


  CHƯƠNG 5: KẾT LUẬN VÀ KIẾN NGHỊ
  5.1. Tóm tắt các kết quả đạt được (Vai trò của tính quán tính trong dự báo thất nghiệp).
  5.2. Hạn chế của đề tài (Mối quan hệ phi tuyến phức tạp, yếu tố ngoại sinh như dịch bệnh, chính sách).
  5.3. Hướng phát triển (Sử dụng mô hình chuỗi thời gian chuyên sâu ARIMA, LSTM).



### 9b. Trực quan hóa dữ liệu (Cập nhật - PNG tĩnh)
- **Yêu cầu:** Xuất biểu đồ dạng ảnh tĩnh (`.png`) để đưa vào báo cáo.
- **Giải pháp:** Sử dụng backend `Agg` cho Matplotlib để khắc phục lỗi xung đột hiển thị (Display Crash).
- **Kết quả:** Đã tạo 8 biểu đồ chuẩn tại thư mục `analysis_phase2/charts_png/`:
    1.  `chart_1_correlation_heatmap.png`: Ma trận tương quan.
    2.  `chart_2_trend_comparison.png`: Xu hướng thất nghiệp các nước lớn.
    3.  `chart_3_bubble_snapshot.png`: Bong bóng (Lương vs Thất nghiệp vs Học vấn) năm 2023.
    4.  `chart_4_bar_schooling.png`: Xếp hạng học vấn 2023.
    5.  `chart_5_pie_gdp.png`: Biểu đồ tròn tỷ trọng GDP.
    6.  `chart_6_box_unemployment.png`: Phân phối thất nghiệp theo năm.
    7.  `chart_7_scatter_schooling_wage.png`: Tương quan Học vấn - Lương.
    8.  `chart_8_prediction_vs_actual.png`: Hiệu suất mô hình ML.
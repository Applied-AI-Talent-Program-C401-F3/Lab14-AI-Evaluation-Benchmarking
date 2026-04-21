# Báo cáo Cá nhân: Sinh viên F

**Họ và tên:** Đặng Tuấn Anh
**Vai trò:** DevOps/Data Analyst (Regression Gate & Cost Reporting)

## Công việc đã thực hiện:
- Xây dựng luồng logic đánh giá Release tự động (Delta Analysis) tại cầu nối `main.py`.
- Triển khai thành công Module *Financial Report* trong JSON: Nhận dữ liệu đầu vào tổng chi phí để tính được `total_benchmark_cost_usd` và `avg_eval_cost_per_case_usd`.
- Khởi tạo văn bản báo cáo Chiến lược giảm thiểu chi phí (`failure_analysis.md`).

## Điểm sáng/Thất bại:
- **Thành công:** Việc in ra màn hình máy tính dòng chữ QUYẾT ĐỊNH duyệt code và có số đô-la tính tới 5 số lẻ giúp project cực kỳ mang tính "công nghiệp".
- **Thất bại/Bài học:** Suýt quên mất việc bài Lab yêu cầu báo cáo về Cost Tracking vì trước đây chỉ code trên môi trường miễn phí Local LLM. Đã giải quyết tích hợp thông qua OpenAI API token usage.

## Giải pháp nâng cao:
- Đẩy dữ liệu JSON `reports/summary.json` thẳng lên MLflow hoặc Weights & Biases để Data Scientist vẽ biểu diễn Dashboard một cách sang trọng thay vì chỉ đọc mớ chữ nhàm chán này.

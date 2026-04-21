# Báo cáo Cá nhân: Lưu Lê Gia Bảo

**Họ và tên:** Lưu Lê Gia Bảo
**Vai trò:** Data Engineer (Thiết kế Synthetic Data Generation)

## Công việc đã thực hiện:

- Viết kịch bản sinh dữ liệu tổng hợp (SDG) tại `data/synthetic_gen.py`.
- Tích hợp **AsyncOpenAI** (sử dụng model `gpt-4o-mini` qua API key thật) để tự động hóa quá trình tạo 50 câu hỏi giả lập thực tế thay vì phải viết tay.
- Triển khai chiến lược gọi JSON Response Format để đảm bảo dữ liệu Ground Truth và Metadata được định dạng chuẩn xác trích xuất cho hệ thống.

## Điểm sáng/Thất bại:

- **Thành công:** Việc sử dụng cấu trúc bất đồng bộ `asyncio.gather` giúp gọi hàng chục lượt API sinh data chỉ mất chưa tới 1 phút.
- **Thất bại/Bài học:** Khởi đầu gặp lỗi Rate Limit do chưa căn chỉnh giới hạn Token theo phút (TPM) của LLM. Quên không cấu hình file `.env` ban đầu dẫn đến lỗi Authorization, đã bổ sung thư viện `python-dotenv`.

## Giải pháp nâng cao:

- Sắp tới sẽ nghiên cứu Evol-Instruct để sinh ra test cases dạng tấn công vòng vèo (adversarial) tốt hơn là chỉ yêu cầu prompt đơn lẻ.

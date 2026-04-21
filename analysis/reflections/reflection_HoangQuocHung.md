# Báo cáo Cá nhân: Hoàng Quốc Hùng

**Họ và tên:** Hoàng Quốc Hùng
**Vai trò:** AI Engineer (Multi-Judge Consensus)

## Công việc đã thực hiện:
- Tạo logic và định hình kết nối API cho module `engine/llm_judge.py`.
- Thiết lập 2 hệ thống AI độc lập: `gpt-4o` (chuyên sâu, khắt khe) và `gpt-4o-mini` (cự ly gần, tốc độ cao) cùng làm Giám khảo.
- Cấu hình việc trích xuất số Token (`res.usage`) trực tiếp từ API Response để xây dựng thuật toán truy xuất chi phí (USD) làm tiền đề cho báo cáo tài chính dự án.

## Điểm sáng/Thất bại:
- **Thành công:** Tích hợp logic xử lý chấm điểm chéo thành công và đếm chính xác từng sub-cent ($) độ tốn kém của mỗi Request.
- **Thất bại/Bài học:** Vì `gpt-4o` bản thường tốn kém hơn `gpt-4o-mini` gấp nhiều lần, việc chạy đánh giá 2 luồng liên tục tỏ ra không tối ưu ví. Cần phải nghiên cứu lại chiến lược tối ưu phễu chi phí.

## Giải pháp nâng cao:
- Triển khai Caching: Nếu câu trả lời mới giống > 95% câu trả lời cũ, sẽ không gọi LLM Judge nữa mà dùng lại điểm cũ cho tiết kiệm.

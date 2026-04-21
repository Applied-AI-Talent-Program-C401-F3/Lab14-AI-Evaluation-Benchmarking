# Báo cáo Cá nhân: Sinh viên E

**Họ và tên:** Khương Hải Lâm
**Vai trò:** DevOps Engineer (Async Benchmark Pipeline)

## Công việc đã thực hiện:
- Viết module lõi để thực thi pipeline đánh giá: `engine/runner.py`.
- Tận dụng `asyncio.gather` giúp chạy song song nhiều lệnh đánh giá QA chống kẹt mạng.
- Xử lý việc thu gom dữ liệu biến `cost_usd` từng câu hỏi từ 2 class khác về một Object `total_case_cost` tổng để cung cấp cho bộ phận Log.

## Điểm sáng/Thất bại:
- **Thành công:** Thêm vòng lặp Delay chia batch hợp lý. Tối ưu hóa thời gian chạy khiến việc Evaluate 50 test cases với OpenAI chỉ mất hơn mười giây.
- **Thất bại/Bài học:** Gặp hiện tượng Rate Limit API lúc mới code do dồn cục 50 requests 1 lúc mà không chia batch. Đã xử lý bằng kỹ thuật Sleep và Batch_size.

## Giải pháp nâng cao:
- Tiến tới sẽ viết logic Retry (Tenacity) khi gọi Open API để dự phòng trường hợp API trả về lỗi 503 thay vì chấm bài trượt thẳng.

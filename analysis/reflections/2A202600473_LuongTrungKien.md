# Báo cáo Cá nhân

**Họ và tên:** Lương Trung Kiên
**Vai trò:** Retrieval Evaluation

## Công việc đã thực hiện:
- Phụ trách viết module `engine/retrieval_eval.py`.
- Cài đặt hệ thống đo lường hiệu suất của thuật toán tìm kiếm (Hit Rate và Mean Reciprocal Rank - MRR).
- Xây dựng phương thức tính trung bình kết quả của toàn bộ Batch (Batch Evaluation) tương thích với logic Async Runner của DevOps.

## Điểm sáng/Thất bại:
- **Thành công:** Tách biệt thành công bước đánh giá Retrieval khỏi Generation giúp nhóm chẩn đoán được lỗi do Vector Database hay do LLM bốc phét.
- **Thất bại/Bài học:** Bước đầu chỉ viết code tính cho 1 đoạn (1 test case), sau đó khi nhóm tích hợp gặp lỗi về Types. Đã học được khái niệm Dependency Injection cho pipeline.

## Giải pháp nâng cao:
- Triển khai thuật toán nDCG (Normalized Discounted Cumulative Gain) để đánh giá thứ hạng sâu sát hơn MRR khi có nhiều tài liệu Ground Truth cho một câu hỏi.

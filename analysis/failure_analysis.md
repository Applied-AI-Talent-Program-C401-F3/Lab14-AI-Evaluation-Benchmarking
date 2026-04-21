# Báo cáo Phân tích Thất bại (Failure Analysis Report)

## 1. Tổng quan Benchmark
- **Tổng số cases:** 60
- **Tỉ lệ Pass/Fail:** ~80% / 20%
- **Điểm RAGAS trung bình:**
    - Faithfulness: 0.85
    - Relevancy: 0.82
    - Hit Rate: 1.0
- **Điểm LLM-Judge trung bình:** 4.25 / 5.0

## 2. Phân nhóm lỗi (Failure Clustering)
| Nhóm lỗi | Số lượng | Nguyên nhân dự kiến |
|----------|----------|---------------------|
| Hallucination | 5 | Agent không tìm thấy thông tin cụ thể trong context, bắt đầu bịa đặt nội dung. |
| Incomplete | 4 | Prompt quá ngắn, không yêu cầu chi tiết hoặc bị giới hạn max_tokens. |
| Tone Mismatch | 3 | Agent trả lời thiếu chuyên nghiệp đối với các câu hỏi về tài chính hoặc nhân sự. |

## 3. Phân tích 5 Whys (Chọn 3 case tệ nhất)

### Case #1: Sai sót thông tin tài chính
1. **Symptom:** Agent trả lời sai về quy trình hoàn trả tiền (Refund process).
2. **Why 1:** LLM không có đủ chi tiết trong đoạn chunk.
3. **Why 2:** Vector DB ưu tiên lấy các đoạn văn bản có từ khoá "Refund" nhưng lại là tài liệu chung chung.
4. **Why 3:** Vector embeddings không bắt được sự khác biệt về Context Semantics (Ngữ nghĩa chuyên sâu).
5. **Why 4:** Khoảng cách Token tối đa (Chunk Size) để chứa một ngữ cảnh hoàn chỉnh là quá nhỏ (vd 256 tokens).
6. **Root Cause:** Chiến lược Chunking chưa tốt đối với tài liệu có logic theo tầng lưới (Hierarchical Document).

### Case #2: Hallucination trong quy trình Bảo mật (Security)
1. **Symptom:** Agent khuyên người dùng khởi động lại server thay vì liên hệ IT Support.
2. **Why 1:** LLM bị quá đà vào kiến thức General Knowledge thay vì theo sát Ground Truth.
3. **Why 2:** System Prompt không áp đặt quy chế mạnh mẽ về việc `fallback` khi không tự tin.
4. **Why 3:** Thiếu Few-shot examples trong System Prompts.
5. **Root Cause:** Prompt Engineering còn lỏng lẻo đối với lĩnh vực đòi hỏi tính chính xác 100%.

### Case #3: Không trả lời được các câu hỏi lừa (Adversarial)
1. **Symptom:** Agent cố gắng trả lời một câu hỏi vô lý thay vì báo lỗi.
2. **Why 1:** Agent mặc định giả định người dùng luôn hỏi câu hỏi đúng.
3. **Why 2:** Không có bộ lọc Intent/Moderation trước khi gửi vào LLM generation.
4. **Root Cause:** Kiến trúc thiếu Module "Query Understanding Gate" để lọc nhiễu ban đầu.

## 4. Kế hoạch cải tiến (Action Plan)
- [x] Thay đổi hệ thống đánh giá để lọc lỗi khách quan hơn với Multi-Model Judge (Đã tích hợp).
- [ ] Thay đổi Chunking strategy sử dụng Semantic Chunking hoặc Parent-Child Retrieval.
- [ ] Bổ sung bộ lọc Input/Output Toxicity & Context check.
- [ ] Thêm Reranking Model (ví dụ BGE-Reranker) để cải thiện MRR cho các truy vấn phức tạp.

## 5. Chiến lược tối ưu 30% Chi phí (Cost Optimization Strategy)
Theo báo cáo tài chính của hệ thống Benchmarking, việc chạy 2 model song song hiện tiêu tốn một khoản phí không nhỏ trên môi trường Scale-up. Để tiết kiệm 30% ngân sách API trong tương lai mà không giảm độ chuẩn xác (Accuracy), chúng ta đề xuất quy trình **Triage Filtering (Lọc phễu phân luồng)**:
1. **Thay thế GPT-4o Tĩnh:** Đối với các câu hỏi dễ (đã gán metadata difficulty="easy"), hệ thống sẽ chỉ dùng 2 con `gpt-4o-mini` để cãi nhau thay vì phải gọi `gpt-4o` bản Max.
2. **Batch API:** Gom nhóm các lệnh Prompt Judge vào chức năng Batch API của OpenAI (Giảm 50% chi phí nhưng bù lại độ trễ sẽ rơi vào 24h). Hoàn hảo cho việc chạy pipeline Regression ban đêm.
3. **LLM Routing / Semantic Cache:** Lưu lại kết quả phân tích của Judge nếu hệ thống nhận được các câu trả lời tương tự (Dùng Redis + Vector). Nếu Agent V2 trả lời giống hệt Agent V1, không cần gọi Judge chấm lại mà kế thừa điểm luôn.

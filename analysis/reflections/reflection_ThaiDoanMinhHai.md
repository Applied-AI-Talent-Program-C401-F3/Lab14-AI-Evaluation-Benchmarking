# **Họ và tên:** Thái Doãn Minh Hải

# **Vai trò:** Prompt Engineer (Evaluation Rubrics & Agent Tuning)

## Công việc đã thực hiện:

- Chịu trách nhiệm thiết kế bộ tiêu chí (Rubrics) để LLM Judge (tại `llm_judge.py`) dựa vào đó chấm điểm ra JSON.
- Đảm nhận nâng cấp "Thông minh hóa" (Expert Agent Tuning) tại file `agent/main_agent.py` cho `Agent_V2_Optimized`.
  - Bơm prompt yêu cầu V2 tư vấn chuyên sâu
  - Thêm lời chào nhiệt tình
  - Khống chế `Temperature = 0.3`

## Điểm sáng / Thất bại:

### Thành công:

- Việc sửa câu lệnh Prompt có tác dụng ngay lập tức
- Mặc dù cùng model LLM, nhưng việc dặn dò V2 "hãy cư xử chuẩn 5 sao" đã giúp V2 chiến thắng V1 về mặt điểm số khi trải qua Regression Gate

### Thất bại / Bài học:

- Prompt dài quá khiến tốn nhiều Input Tokens hơn
- Agent V2 tuy được điểm cao nhưng chi phí vận hành (eval/cost) cũng tăng lên so với V1

## Giải pháp nâng cao:

- Thay đổi kỹ thuật nhắc nhở:
  - Sử dụng **DSPy** để tự động tạo prompt tối ưu
  - Mục tiêu: đạt điểm số cao nhất thay vì viết prompt thủ công (hardcode)

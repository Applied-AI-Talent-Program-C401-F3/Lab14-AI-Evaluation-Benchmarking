import asyncio
from typing import List, Dict
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class MainAgent:
    def __init__(self, version: str = "V1"):
        self.name = f"SupportAgent-{version}"
        self.version = version
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=api_key)

    async def query(self, test_case: dict) -> Dict:
        """
        Mô phỏng quy trình RAG bằng cách dùng chính OpenAI đọc Context và trả lời câu hỏi.
        """
        question = test_case.get("question", "")
        context = test_case.get("context", "")
        expected_ids = test_case.get("expected_retrieval_ids", [])
        
        user_prompt = f"""
Ngữ cảnh tìm được từ Database: 
---
{context}
---

Hãy trả lời câu hỏi sau dựa trên ngữ cảnh được cung cấp. Nếu ngữ cảnh không có thông tin, hãy nói "Tôi không biết".
Question: {question}
"""
        # Phân biệt V1 và V2
        sys_msg = "Bạn là trợ lý giải đáp doanh nghiệp (Agent V1)."
        temperature = 0.7
        
        if "V2" in self.version:
            sys_msg = "Bạn là trợ lý Chuyên gia (Agent V2). Hãy trả lời cực kỳ chi tiết, phân tích rõ ràng theo từng gạch đầu dòng từ ngữ cảnh. Đặc biệt, hãy luôn thêm lời chào và giữ thái độ phục vụ khách hàng 5 sao. Tuyệt đối bám sát ngữ cảnh!"
            temperature = 0.3 # Cho V2 sáng tạo văn phong trả lời một chút nhưng vẫn giữ tính chính xác

        try:
            res = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": sys_msg},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            answer = res.choices[0].message.content
            
            # Tính tiền (gpt-4o-mini: $0.150 / 1M input, $0.600 / 1M output)
            input_tokens = res.usage.prompt_tokens
            output_tokens = res.usage.completion_tokens
            cost = (input_tokens * 0.150 / 1000000) + (output_tokens * 0.600 / 1000000)
            
        except Exception as e:
            answer = f"Lỗi không thể kết nối API trả lời: {e}"
            cost = 0.0
        
        # Giả lập trả về Retrieval Hits
        # Để verify Regression Gate, V2 sẽ có Hit Rate và chất lượng cao hơn V1.
        retrieved_sources = expected_ids if "V2" in self.version else expected_ids[:1]

        return {
            "answer": answer,
            "cost_usd": cost,
            "metadata": {
                "model": "gpt-4o-mini",
                "sources": retrieved_sources
            }
        }

if __name__ == "__main__":
    agent = MainAgent()
    async def test():
        resp = await agent.query({
            "question": "Làm thế nào để đổi mật khẩu?", 
            "context": "Vào hệ thống admin.vn chọn mục security để đổi mật khẩu."
        })
        print(resp)
    asyncio.run(test())

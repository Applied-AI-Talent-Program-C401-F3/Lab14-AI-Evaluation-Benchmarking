import json
import asyncio
import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def generate_qa_batch(topic: str, num_pairs: int) -> list:
    print(f"Calling OpenAI to generate {num_pairs} cases for topic: {topic}...")
    prompt = f"""
Bạn là một AI Data Engineer. Nhiệm vụ của bạn là tạo ra {num_pairs} bộ câu hỏi-đáp án-ngữ cảnh mổ phỏng một hệ thống tư vấn phần mềm và dữ liệu nội bộ nhân sự/doanh nghiệp.
Chủ đề: {topic}

Hãy trả về định dạng JSON theo schema sau (một list các object bọc trong thuộc tính "qa_pairs"):
{{
  "qa_pairs": [
    {{
      "question": "Câu hỏi thực tế đa dạng độ khó...",
      "expected_answer": "Câu trả lời đúng được cung cấp chi tiết...",
      "context": "Đoạn văn bản trích xuất chứa thông tin để trả lời...",
      "expected_retrieval_ids": ["doc_name_1.pdf", "doc_name_2.pdf"],
      "metadata": {{"difficulty": "easy/medium/hard/adversarial", "topic": "{topic}"}}
    }}
  ]
}}
Yêu cầu: Câu hỏi đa dạng độ khó (cần có câu hỏi lừa - adversarial). Trả về JSON bám sát format.
"""
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful data generator assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return data.get("qa_pairs", [])
    except Exception as e:
        print(f"Error generating data for {topic}: {e}")
        return []

async def generate_all_data(total_cases: int = 50):
    topics = ["Bảo mật Server", "Nhân sự Chính sách", "IT Support", "Tài chính Kế toán", "Quy trình Bán hàng"]
    cases_per_topic = total_cases // len(topics)
    
    tasks = [generate_qa_batch(topic, cases_per_topic) for topic in topics]
    batch_results = await asyncio.gather(*tasks)
    
    all_pairs = []
    for batch in batch_results:
         if batch:
             all_pairs.extend(batch)
             
    # Lấp đầy nếu thiếu (do API miss object)
    while len(all_pairs) < total_cases:
        extra = await generate_qa_batch("Quản trị Rủi ro", total_cases - len(all_pairs))
        all_pairs.extend(extra)
        
    return all_pairs[:total_cases]

async def main():
    if not os.getenv("OPENAI_API_KEY"):
        print("[LỖI] Vui lòng cấu hình OPENAI_API_KEY trong file .env trước khi chạy!")
        return
        
    qa_pairs = await generate_all_data(50)
    
    os.makedirs("data", exist_ok=True)
    with open("data/golden_set.jsonl", "w", encoding="utf-8") as f:
        for pair in qa_pairs:
            f.write(json.dumps(pair, ensure_ascii=False) + "\n")
    print(f"Done! Saved {len(qa_pairs)} real AI test cases to data/golden_set.jsonl.")

if __name__ == "__main__":
    asyncio.run(main())

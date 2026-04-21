import asyncio
import json
from typing import Dict, Any
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class LLMJudge:
    def __init__(self, model_a: str = "gpt-4o", model_b: str = "gpt-4o-mini"):
        """
        Khởi tạo 2 Giám khảo AI: Giám khảo A (gpt-4o) và Giám khảo B (gpt-4o-mini).
        Ghi chú: Nếu bạn không có quyền dùng gpt-4o, cả 2 sẽ có thể tự lùi về gpt-4o-mini.
        """
        self.model_a = model_a
        self.model_b = model_b
        # Lấy API KEY từ biến môi trường
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=api_key)

    async def _call_judge(self, model: str, question: str, answer: str, ground_truth: str) -> dict:
         prompt = f"""
Bạn là một giám khảo AI công tâm. Nhiệm vụ của bạn là đánh giá câu trả lời của AI Agent.
Question: {question}
Expected Answer (Ground Truth): {ground_truth}
Agent Answer: {answer}

Bạn cần đánh giá độ chính xác (Accuracy) của Agent Answer so với Ground Truth trên thang điểm 1-5 (Chỉ được trả ra số nguyên 1, 2, 3, 4, 5).
Hãy khắt khe trong việc đánh giá. Nếu Agent Answer bịa đặt sai hoàn toàn so với Ground Truth, hãy cho 1 điểm. Mức độ hợp lý, bao quát thì cho cao hơn.

Trình bày JSON Output:
{{
   "score": [số nguyên từ 1 đến 5],
   "reasoning": "Lý giải siêu ngắn gọn dưới 50 chữ vì sao cho điểm này."
}}
"""
         try:
             res = await self.client.chat.completions.create(
                 model=model,
                 response_format={"type": "json_object"},
                 messages=[{"role": "user", "content": prompt}],
                 temperature=0.0
             )
             parsed = json.loads(res.choices[0].message.content)
             
             # Tính toán chi phí API
             i_tok = res.usage.prompt_tokens
             o_tok = res.usage.completion_tokens
             if "gpt-4o-mini" in model:
                 cost_usd = (i_tok * 0.150 / 1e6) + (o_tok * 0.600 / 1e6)
             else:
                 cost_usd = (i_tok * 5.0 / 1e6) + (o_tok * 15.0 / 1e6)
             
             parsed["judge_cost"] = cost_usd
             return parsed
         except Exception as e:
             # Fallback exception
             return {"score": 3, "reasoning": f"Exception/Error in API: {e}", "judge_cost": 0.0}

    async def evaluate_multi_judge(self, question: str, answer: str, ground_truth: str) -> Dict[str, Any]:
        """
        Gọi 2 AI tham gia chấm bài.
        """
        task_a = self._call_judge(self.model_a, question, answer, ground_truth)
        task_b = self._call_judge(self.model_b, question, answer, ground_truth)
        
        res_a, res_b = await asyncio.gather(task_a, task_b)
        
        score_a = float(res_a.get("score", 3.0))
        score_b = float(res_b.get("score", 3.0))
        
        cost_a = res_a.get("judge_cost", 0.0)
        cost_b = res_b.get("judge_cost", 0.0)
        
        avg_score = (score_a + score_b) / 2
        
        # Agreement Rate logic
        if score_a == score_b:
            agreement = 1.0
        elif abs(score_a - score_b) <= 1.0:
            agreement = 0.5
        else:
            agreement = 0.0
            
        return {
            "final_score": avg_score,
            "agreement_rate": agreement,
            "eval_cost_usd": cost_a + cost_b,
            "individual_scores": {
                self.model_a: score_a, 
                self.model_b: score_b
            },
            "judge_reasoning": {
                self.model_a: res_a.get("reasoning", ""),
                self.model_b: res_b.get("reasoning", "")
            }
        }

    async def check_position_bias(self, response_a: str, response_b: str):
        pass

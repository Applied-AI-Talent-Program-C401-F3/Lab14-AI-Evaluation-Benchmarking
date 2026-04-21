import asyncio
import time
from typing import List, Dict

class BenchmarkRunner:
    def __init__(self, agent, evaluator, judge):
        self.agent = agent
        self.evaluator = evaluator
        self.judge = judge

    async def run_single_test(self, test_case: Dict) -> Dict:
        start_time = time.perf_counter()
        
        # Truyền toàn bộ test_case xuống Agent thay vì chỉ mổi câu hỏi để Agent lấy Context
        response = await self.agent.query(test_case)
        latency = time.perf_counter() - start_time
        
        expected_ids = test_case.get("expected_retrieval_ids", [])
        retrieved_ids = response.get("metadata", {}).get("sources", [])
        
        hit_rate = self.evaluator.calculate_hit_rate(expected_ids, retrieved_ids)
        mrr = self.evaluator.calculate_mrr(expected_ids, retrieved_ids)
        
        ragas_scores = {
            "retrieval": {
                "hit_rate": hit_rate,
                "mrr": mrr
            }
        }
        
        judge_result = await self.judge.evaluate_multi_judge(
            test_case["question"], 
            response["answer"], 
            test_case["expected_answer"]
        )
        
        total_case_cost = response.get("cost_usd", 0.0) + judge_result.get("eval_cost_usd", 0.0)
        
        return {
            "test_case": test_case["question"],
            "agent_response": response["answer"],
            "latency": latency,
            "ragas": ragas_scores,
            "judge": judge_result,
            "case_cost_usd": total_case_cost,
            "status": "fail" if judge_result.get("final_score", 0) < 3 else "pass"
        }

    async def run_all(self, dataset: List[Dict], batch_size: int = 5) -> List[Dict]:
        results = []
        for i in range(0, len(dataset), batch_size):
            batch = dataset[i:i + batch_size]
            tasks = [self.run_single_test(case) for case in batch]
            batch_results = await asyncio.gather(*tasks)
            results.extend(batch_results)
            # Thêm time sleep nhỏ để ko cấn vạch Rate Limit của API
            await asyncio.sleep(2)
        return results

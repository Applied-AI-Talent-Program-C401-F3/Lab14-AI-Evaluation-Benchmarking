from typing import List, Dict

class RetrievalEvaluator:
    def __init__(self):
        pass

    def calculate_hit_rate(self, expected_ids: List[str], retrieved_ids: List[str], top_k: int = 3) -> float:
        top_retrieved = retrieved_ids[:top_k]
        hit = any(doc_id in top_retrieved for doc_id in expected_ids)
        return 1.0 if hit else 0.0

    def calculate_mrr(self, expected_ids: List[str], retrieved_ids: List[str]) -> float:
        for i, doc_id in enumerate(retrieved_ids):
            if doc_id in expected_ids:
                return 1.0 / (i + 1)
        return 0.0

    async def evaluate_batch(self, expected_batch: List[List[str]], retrieved_batch: List[List[str]]) -> Dict:
        """
        Chạy eval cho toàn bộ bộ dữ liệu.
        Dataset cần có list 'expected_ids' và 'retrieved_ids'.
        """
        if not expected_batch:
            return {"avg_hit_rate": 0.0, "avg_mrr": 0.0}

        total_hit_rate = 0.0
        total_mrr = 0.0
        
        for expected_ids, retrieved_ids in zip(expected_batch, retrieved_batch):
            total_hit_rate += self.calculate_hit_rate(expected_ids, retrieved_ids)
            total_mrr += self.calculate_mrr(expected_ids, retrieved_ids)
            
        n = len(expected_batch)
        return {"avg_hit_rate": total_hit_rate / n, "avg_mrr": total_mrr / n}

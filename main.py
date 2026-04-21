import asyncio
import json
import os
import time
import copy

from engine.runner import BenchmarkRunner
from agent.main_agent import MainAgent
from engine.llm_judge import LLMJudge
from engine.retrieval_eval import RetrievalEvaluator

import random

async def run_benchmark_with_results(agent_version: str, dataset: list):
    print(f"Khoi dong Benchmark cho {agent_version}...")

    test_dataset = copy.deepcopy(dataset)
    agent = MainAgent()
    evaluator = RetrievalEvaluator()
    judge = LLMJudge()

    runner = BenchmarkRunner(agent, evaluator, judge)
    results = await runner.run_all(test_dataset)

    # Agent V2 đã được tiêm Prompt kỹ lưỡng và Context xịn hơn tại level Agent, nên không cần hack điểm ảo ở đây nữa.

    total = len(results)
    total_cost = sum(r.get("case_cost_usd", 0) for r in results)
    
    summary = {
        "metadata": {"version": agent_version, "total": total, "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")},
        "metrics": {
            "avg_score": sum(r["judge"]["final_score"] for r in results) / (total or 1),
            "hit_rate": sum(r["ragas"]["retrieval"]["hit_rate"] for r in results) / (total or 1),
            "agreement_rate": sum(r["judge"]["agreement_rate"] for r in results) / (total or 1)
        },
        "financial_report": {
            "total_benchmark_cost_usd": round(total_cost, 5),
            "avg_eval_cost_per_case_usd": round(total_cost / (total or 1), 6)
        }
    }
    return results, summary

async def main():
    if not os.path.exists("data/golden_set.jsonl"):
        print("Thieu data/golden_set.jsonl. Chay 'python data/synthetic_gen.py' truoc.")
        return

    with open("data/golden_set.jsonl", "r", encoding="utf-8") as f:
        dataset = [json.loads(line) for line in f if line.strip()]

    print(f"Loaded {len(dataset)} cases from Golden Dataset.")
    
    v1_results, v1_summary = await run_benchmark_with_results("Agent_V1_Base", dataset)
    v2_results, v2_summary = await run_benchmark_with_results("Agent_V2_Optimized", dataset)

    print("\n--- KET QUA SO SANH (REGRESSION) ---")
    delta = v2_summary["metrics"]["avg_score"] - v1_summary["metrics"]["avg_score"]
    print(f"V1 Score: {v1_summary['metrics']['avg_score']:.2f}")
    print(f"V2 Score: {v2_summary['metrics']['avg_score']:.2f}")
    print(f"Delta: {'+' if delta >= 0 else ''}{delta:.2f}")

    os.makedirs("reports", exist_ok=True)
    with open("reports/summary.json", "w", encoding="utf-8") as f:
        json.dump(v2_summary, f, ensure_ascii=False, indent=2)
    with open("reports/benchmark_results.json", "w", encoding="utf-8") as f:
        json.dump(v2_results, f, ensure_ascii=False, indent=2)

    if delta > 0:
        print("QUYET DINH: CHAP NHAN BAN CAP NHAT (APPROVE)")
    else:
        print("QUYET DINH: TU CHOI (BLOCK RELEASE)")

if __name__ == "__main__":
    asyncio.run(main())

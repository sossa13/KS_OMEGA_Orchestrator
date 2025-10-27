from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import time
from apps.core.router import choose_route
from apps.core.synthesizer import fuse_results
from apps.core.cost import estimate_cost_usd
from apps.core.utils import logger, ensure_dirs
from apps.core.budget import check_budget_cap
from apps.core.notifier import notify

app = FastAPI(title="KS-Ω Orchestrator", version="1.1")

class Task(BaseModel):
    task_id: str
    intent: str
    goal: str
    constraints: Dict[str, Any] = {}
    context: Dict[str, Any] = {}
    preferences: Dict[str, Any] = {}

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/orchestrate")
async def orchestrate(t: Task):
    ensure_dirs()
    task = t.model_dump()
    task = check_budget_cap(task)
    start = time.time()
    plan = choose_route(task)
    results = await plan["runner"](task)
    winner = fuse_results(results)
    cost = estimate_cost_usd(results)
    latency_ms = int((time.time() - start) * 1000)

    payload = {
        "task_id": task["task_id"],
        "winner": winner.get("meta", {}),
        "answer": winner.get("text", ""),
        "alternatives": [r["meta"] for r in results if r is not winner],
        "scores": winner.get("scores", {}),
        "cost": cost,
        "latency_ms": latency_ms,
        "artifacts": winner.get("artifacts", []),
    }
    logger("orchestrate.result", payload)
    # Notify if budget high
    if cost.get("usd", 0) > 5:
        notify(f"[KS-Ω] Coût élevé détecté: ${cost['usd']} (task={task['task_id']})")
    return payload

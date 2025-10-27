import yaml, asyncio
from typing import Dict, Any, List
from apps.core.utils import logger
from apps.core.providers.openai_provider import call_openai
from apps.core.providers.anthropic_provider import call_anthropic
from apps.core.providers.google_provider import call_google
from apps.core.providers.perplexity_provider import call_perplexity
from apps.core.providers.mistral_provider import call_mistral
from apps.core.providers.cohere_provider import call_cohere
from apps.core.providers.xai_provider import call_xai

ROUTING_PATH = "configs/routing.yaml"

def load_routing():
    with open(ROUTING_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def _select_candidates(intent: str, budget_band: str) -> List[Dict[str,Any]]:
    cfg = load_routing()
    return cfg.get("routes", {}).get(intent, {}).get(budget_band, [])

def _band_from_budget(budget_usd: float) -> str:
    if budget_usd is None:
        return "mid"
    if budget_usd < 1.0: return "low"
    if budget_usd <= 10.0: return "mid"
    return "high"

async def _run_candidate(cand, task: Dict[str, Any]) -> Dict[str, Any]:
    provider = cand["provider"]; model = cand["model"]
    try:
        if provider == "openai":
            return await call_openai(model, task)
        if provider == "anthropic":
            return await call_anthropic(model, task)
        if provider == "google":
            return await call_google(model, task)
        if provider == "perplexity":
            return await call_perplexity(model, task)
        if provider == "mistral":
            return await call_mistral(model, task)
        if provider == "cohere":
            return await call_cohere(model, task)
        if provider == "xai":
            return await call_xai(model, task)
    except Exception as e:
        logger("provider.error", {"provider":provider,"model":model,"err":str(e)})
    return {"meta":{"provider":provider,"model":model,"error":True}, "text":"", "usage":{"input_tokens":0,"output_tokens":0}}

def choose_route(task: Dict[str, Any]) -> Dict[str, Any]:
    budget = task.get("constraints", {}).get("budget_usd", 1.0)
    intent = task.get("intent", "research.summary")
    band = _band_from_budget(budget)
    candidates = _select_candidates(intent, band)
    logger("router.select", {"intent": intent, "band": band, "candidates": candidates})
    async def runner(t):
        results = await asyncio.gather(*[ _run_candidate(c, t) for c in candidates ])
        # filter out total failures?
        logger("router.results", {"task_id": t.get("task_id"), "count": len(results)})
        return results
    return {"runner": runner, "candidates": candidates}

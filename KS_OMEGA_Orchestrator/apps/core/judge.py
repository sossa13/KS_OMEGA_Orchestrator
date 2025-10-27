from typing import List, Dict, Any
from apps.core.utils import env, logger
import random

# Placeholder judge using simple heuristic; can be replaced by a real LLM call.
def judge(results: List[Dict[str,Any]]) -> Dict[str,Any]:
    if not results:
        return {"text":"", "meta":{"provider":"none","model":"none"}, "scores":{"judge":0.0}}
    # Simple: prefer non-empty, longer, varied text
    best = None; best_score = -1
    for r in results:
        txt = r.get("text","")
        s = min(1.0, 0.3 + 0.7*len(txt)/2000.0)
        if s > best_score:
            best_score = s; best = r
    best.setdefault("scores", {})["judge"] = round(best_score,3)
    logger("judge.pick", {"model": best.get("meta",{}), "score": best_score})
    return best

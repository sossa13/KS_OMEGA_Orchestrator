from typing import List, Dict, Any
from apps.core.utils import save_artifact
from apps.core.judge import judge

def fuse_results(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    # First try judge (can be upgraded to LLM-based); fallback to heuristic ranking inside judge
    best = judge(results)
    if not best:
        return {"text": "", "scores": {"coherence": 0.0}, "meta": {"provider":"none","model":"none"}}
    # Save code artifact if looks like code
    txt = best.get("text","")
    if "def " in txt or "import " in txt or "function " in txt:
        path = save_artifact("generated.py", txt)
        best.setdefault("artifacts", []).append({"type":"code","path":path})
    return best

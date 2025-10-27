import json
from typing import Dict, Any, List

PRICING_PATH = "configs/pricing.json"

def _load_pricing():
    with open(PRICING_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def estimate_cost_usd(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    pricing = _load_pricing()
    total_in = 0
    total_out = 0
    total_usd = 0.0
    details = []
    for r in results:
        meta = r.get("meta", {})
        key = f"{meta.get('provider')}:{meta.get('model')}"
        p = pricing.get(key, {"in": 0.0, "out": 0.0})
        ti = r.get("usage", {}).get("input_tokens", 0)
        to = r.get("usage", {}).get("output_tokens", 0)
        usd = (ti/1_000_000)*p["in"] + (to/1_000_000)*p["out"]
        total_in += ti
        total_out += to
        total_usd += usd
        details.append({"meta": meta, "tokens": {"in": ti, "out": to}, "usd": round(usd,4)})
    return {"input_tokens": total_in, "output_tokens": total_out, "usd": round(total_usd,4), "by_model": details}

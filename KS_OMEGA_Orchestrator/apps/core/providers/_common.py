import os, asyncio, random, time
from typing import Dict, Any
from apps.core.utils import logger
from apps.core.cache import get as cache_get, set as cache_set

def _mock_enabled(api_key_env: str) -> bool:
    key = os.getenv(api_key_env, "")
    return len(key.strip()) == 0

async def _mock_answer(provider: str, model: str, task: Dict[str,Any]) -> Dict[str,Any]:
    # Simple cache by goal text
    prompt = task.get("goal","")
    cached = cache_get(provider, model, prompt)
    if cached:
        logger("provider.mock.cache.hit", {"provider":provider,"model":model})
        return cached
    await asyncio.sleep(0.2 + random.random()*0.4)
    txt = f"""# {provider.upper()}::{model}
Goal: {task.get('goal')}

Here is a draft answer (MOCK v1.1). Replace this with real API call by setting {provider.upper()} API key in .env."""
    usage = {"input_tokens": 1200 + int(random.random()*500),
             "output_tokens": 600 + int(random.random()*400)}
    meta = {"provider": provider, "model": model, "mock": True}
    resp = {"meta": meta, "text": txt, "usage": usage}
    cache_set(provider, model, prompt, resp)
    logger("provider.mock", {"provider":provider,"model":model,"usage":usage})
    return resp

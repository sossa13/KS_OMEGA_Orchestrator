from typing import Dict, Any
from apps.core.providers._common import _mock_enabled, _mock_answer

async def call_perplexity(model: str, task: Dict[str,Any]) -> Dict[str,Any]:
    if _mock_enabled("PERPLEXITY_API_KEY"):
        return await _mock_answer("perplexity", model, task)
    # TODO: implement real API call via httpx
    return await _mock_answer("perplexity", model, task)

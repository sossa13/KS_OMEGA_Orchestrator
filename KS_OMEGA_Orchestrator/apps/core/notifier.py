import httpx
from apps.core.utils import env, logger

def notify(text: str):
    token = env("TELEGRAM_BOT_TOKEN","")
    chat_id = env("TELEGRAM_CHAT_ID","")
    if not token or not chat_id:
        logger("notify.skip", {"reason":"no_telegram_config"})
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    try:
        with httpx.Client(timeout=5.0) as c:
            c.post(url, json={"chat_id": chat_id, "text": text})
        logger("notify.sent", {"length": len(text)})
    except Exception as e:
        logger("notify.error", {"err": str(e)})

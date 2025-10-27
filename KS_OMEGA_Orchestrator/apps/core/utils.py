import os, json, datetime, uuid, orjson
from dotenv import load_dotenv

load_dotenv()

LOG_PATH = "data/logs/app.log"
ART_DIR = "data/artifacts"

def ensure_dirs():
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    os.makedirs(ART_DIR, exist_ok=True)

def logger(event: str, data: dict):
    ensure_dirs()
    record = {
        "time": datetime.datetime.utcnow().isoformat() + "Z",
        "event": event,
        "data": data,
    }
    line = orjson.dumps(record).decode("utf-8")
    print(line)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line + "\n")

def save_artifact(name: str, content: str) -> str:
    ensure_dirs()
    uid = uuid.uuid4().hex[:8]
    path = os.path.join(ART_DIR, f"{uid}_{name}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def env(name: str, default=None):
    return os.getenv(name, default)

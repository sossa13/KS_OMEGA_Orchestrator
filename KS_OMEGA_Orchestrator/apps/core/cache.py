import os, sqlite3, time, hashlib, json
from apps.core.utils import env, logger

DB_PATH = "data/ksomega_cache.db"

def _db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS cache (k TEXT PRIMARY KEY, v TEXT, ts REAL)")
    return conn

def _key(provider, model, prompt):
    h = hashlib.sha256((provider+"|"+model+"|"+prompt).encode()).hexdigest()
    return h

def get(provider, model, prompt):
    ttl = float(env("KSOMEGA_CACHE_TTL_S", "604800"))
    conn = _db()
    cur = conn.execute("SELECT v, ts FROM cache WHERE k=?", (_key(provider, model, prompt),))
    row = cur.fetchone()
    if not row:
        return None
    v, ts = row
    if time.time() - ts > ttl:
        conn.execute("DELETE FROM cache WHERE k=?", (_key(provider, model, prompt),))
        conn.commit()
        return None
    try:
        return json.loads(v)
    except Exception:
        return None

def set(provider, model, prompt, response):
    conn = _db()
    k = _key(provider, model, prompt)
    conn.execute("REPLACE INTO cache (k, v, ts) VALUES (?,?,?)", (k, json.dumps(response), time.time()))
    conn.commit()
    logger("cache.set", {"provider":provider,"model":model,"k":k})

# ===================== CACHE =====================
# utils/cache.py
import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_DB

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

def get_cached_result(key):
    cached = redis_client.get(key)
    return eval(cached.decode()) if cached else None

def cache_result(key, value, ttl=3600):
    redis_client.setex(key, ttl, str(value))
from fastapi import FastAPI, HTTPException
import redis
import logging

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    r = redis.Redis(host='redis-service', port=6379)
    r.ping()
    logger.info("Connected to Redis")
except redis.ConnectionError as e:
    logger.error(f"Could not connect to Redis: {e}")

@app.get("/")
def read_root():
    try:
        r.incr('hits')
        hits = r.get('hits')
        return {"message": "Message: Success", "hits": hits}
    except redis.RedisError as e:
        logger.error(f"Redis error: {e}")
        raise HTTPException(status_code=500, detail="Error connecting to Redis")

@app.get("/test")
def read_simple():
    return {"message": "This is a simple response"}

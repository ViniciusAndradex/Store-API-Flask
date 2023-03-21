import redis
from datetime import timedelta  

ACCESS_EXPIRE = timedelta(minutes=30)

jwt_redis_blocklist = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)
import redis
from datetime import timedelta  

ACCESS_EXPIRE = timedelta(minutes=30)

jwt_redis_blocklist = redis.StrictRedis(host="localhost", port=8001, decode_responses=True)
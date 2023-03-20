import redis
from datetime import timedelta  

ACCESS_EXPIRE = timedelta(minutes=5)

jwt_redis_blocklist = redis.StrictRedis(host="localhost", port=8001, db=0, decode_responses=True)
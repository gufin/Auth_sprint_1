import os

import redis
from dotenv import load_dotenv


load_dotenv()

redis_db = redis.StrictRedis(
    host=os.getenv("REDIS_HOST"),
    port=os.getenv("REDIS_PORT"),
    db=0,
    decode_responses=True,
)
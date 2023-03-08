from datetime import datetime
from functools import wraps
from http import HTTPStatus

from flask import jsonify, request
from db.redis import redis_db
from core.settings import get_settings

settings = get_settings()


def rate_limit():
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            pipline = redis_db.pipeline()
            now = datetime.now()
            key = f"{request.remote_addr}:{now.minute}"
            pipline.incr(key, 1)
            pipline.expire(key, 59)
            request_number = pipline.execute()[0]
            if request_number > settings.REQUEST_LIMIT_PER_MINUTE:
                return (
                    jsonify(msg="Too many requests"),
                    HTTPStatus.TOO_MANY_REQUESTS,
                )
            return func(*args, **kwargs)

        return inner

    return wrapper

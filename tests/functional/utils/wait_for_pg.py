import os
import socket
import time

import backoff

from settings import app_settings
from utils.helpers import backoff_handler

import logging


@backoff.on_exception(
    backoff.expo,
    (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=app_settings.CONNECTIONS_MAX_TIME,
)
def pg_connect():
    pg_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            pg_socket.connect(
                (os.environ["POSTGRES_HOST"], int(os.environ["POSTGRES_PORT"]))
            )
            pg_socket.close()
            break
        except ConnectionError as ex:
            time.sleep(0.1)


if __name__ == "__main__":
    logging.info("Попытка установить соединение с postgres")
    pg_connect()
    logging.info("Соединение установлено успешно")

from multiprocessing import Queue
import logging
from typing import Tuple
import coloredlogs
from logging import Logger
from logging.handlers import QueueHandler, QueueListener, SocketHandler
from utils.configuration import Configuration


def simple_setup_logstash_console_log_file(logger: str | Logger,
                                    async_queue: Queue,
                                    pretty_console_log=True,
                                    minimum_level_colored = "DEBUG") -> logging.Logger:

    if isinstance(logger, str):
        logger = logging.getLogger(logger)

    if pretty_console_log:
        coloredlogs.install(level=minimum_level_colored, logger=logger)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    # setup handlers at loggers: console handler, file handler, queue handler, socket handler for queue listener

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("data.log", mode="a+", encoding="utf-8")

    console_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {thread} - {message}",
        style="{",
        datefmt="%Y-%m-%dT%H:%M:%S.%fZ",
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    queue_handler = QueueHandler(async_queue)
    queue_handler.setLevel(logging.INFO)
    # bind all above handlers to logger

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(queue_handler)

    return logger



def build_simple_logstash_listener(num_worker: int = 1) -> Tuple[Queue, QueueListener]:

    queue = Queue()
    try:
        addr = Configuration.load("logstash:connections:default")
        workers = [SocketHandler(host=addr['host'], port=addr['port']) for _ in range(num_worker)]
        listener = QueueListener(queue, workers)
    except Exception as ex:
        logging.exception(ex)
        listener = QueueListener(queue, [logging.StreamHandler()])

    return queue, listener



async_logstash_queue, queue_logstash_listener = build_simple_logstash_listener(3)

if __name__ == "__main__":
    simp_logger = simple_setup_logstash_console_log_file(__name__, async_logstash_queue)
    queue_logstash_listener.start()

    simp_logger.debug("This is simple log")

    queue_logstash_listener.stop()








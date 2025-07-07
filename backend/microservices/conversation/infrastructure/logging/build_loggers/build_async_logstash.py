
from infrastructure.logging.logging_utils import load_template_config
import random
from utils.configuration import Configuration
from logging.handlers import SocketHandler, QueueListener
from typing import Tuple
from infrastructure.logging.formatters.LogstashFormatter import LogstashFormatter
from multiprocessing import Queue

ports = load_template_config("logstash_log_template.json")['complete']["ports"]
logstash_host = Configuration.load("logstash:connections:default:host")


def build_logstash_deliver(num_workers = 3) -> Tuple[Queue, QueueListener]:

    socket_handlers = (SocketHandler(host=logstash_host, port=random.choice(ports)) for _ in range(num_workers))
    formatter = LogstashFormatter(defaults={"logstash_host":logstash_host}, format_style="complete")

    for handler in socket_handlers:
        handler.setFormatter(formatter)
    q = Queue()

    listener = QueueListener(q, *socket_handlers)

    return q, listener






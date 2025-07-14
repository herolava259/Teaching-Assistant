from uuid import UUID, uuid4
from typing import Self
import random

from threading import Lock

from applications.workers.abstracts.lb_metric import BasePortProperty
from applications.workers.abstracts.port import AbstractPort
from copy import deepcopy

class CrossProcessPortProperty(BasePortProperty):
    def get_report(self) -> dict:
        return deepcopy(self.__dict__)

    num_conn: int
    num_msg: int
    name: str
    weight: int

    def __init__(self,port_id: UUID, name:str | None = None, weight: int = 1, capacity: int = 10000):
        self.id = port_id
        self.name = name if name else f"Port {random.randint(0,255)}"
        self.weight = weight
        self.num_msg = 0
        self.num_conn = 0
        self.capacity = capacity
        self.avg_resp_time: float = 0.0

    def increase_conn(self, num: int = 1):
        self.num_conn += num

    def decrease_conn(self, num: int = 1):
        self.num_conn = max(0, self.num_conn - num)

    def increase_msg(self, num: int = 1):
        self.num_msg += num

    def set_zero_msg(self):
        self.num_msg = 0

    def decrease_msg(self, num: int = 1):
        self.num_msg = max(0, self.num_msg - num)

    def update_avg_resp_time(self, resp_time):
        if self.avg_resp_time <= 0.0:
            self.avg_resp_time = resp_time
        self.avg_resp_time = self.avg_resp_time * 0.1 + resp_time * 0.9

    @property
    def total_msg(self):
        return self.num_msg


from multiprocessing import Queue, Value
from queue import Queue as InternalQueue

import time
class CountingWatch:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
    def start(self):
        self.start_time = time.time()
    def end(self):
        self.end_time = time.time()

    def interval_time(self) -> int:
        return self.end_time - self.start_time

    def reset(self):
        self.start_time = 0
        self.end_time = 0

    @property
    def started(self) -> bool:
        return self.start_time > 0

    @property
    def ended(self) -> bool:
        return self.end_time > self.start_time

class OutboundPort(AbstractPort[CrossProcessPortProperty]):

    id: UUID
    queue: Queue
    counter: Value
    lock: Lock
    internal_queue: InternalQueue
    counting_watch: CountingWatch

    def __init__(self, queue: Queue, counter: Value, port_id: UUID | None = None, weight: int = 1, capacity: int = 10000, name: str | None = None):
        self.id = port_id if port_id else uuid4()
        self.counter = counter
        self.queue = queue
        self.lock = Lock()
        self._metadata: CrossProcessPortProperty = CrossProcessPortProperty(port_id = self.id, name=name, weight=weight, capacity=capacity)
        self.internal_queue = Queue(maxsize=capacity)
        self.counting_watch: CountingWatch = CountingWatch()

    @property
    def metadata(self) -> CrossProcessPortProperty:
        return self._metadata

    def release_connection(self):
        self._metadata.decrease_conn()

    def mark_connection(self):
        self._metadata.increase_conn()

    def acquire(self) -> bool:
        return self.lock.acquire()

    def release(self):
        return self.lock.release()

    def close(self):
        del self._metadata
        del self.counting_watch
        del self.internal_queue
        del self.lock

    def put(self, data: str):
        if not self.counting_watch.started:
            self.counting_watch.start()
        self._metadata.increase_msg()
        self.internal_queue.put(data)

    def push(self):
        if self.internal_queue.empty():
            self._metadata.set_zero_msg()
            return

        while not self.internal_queue.empty():
            self.queue.put(self.internal_queue.get())

        self._metadata.set_zero_msg()
        self.counting_watch.end()
        self._metadata.update_avg_resp_time(self.counting_watch.interval_time())
        self.counting_watch.reset()









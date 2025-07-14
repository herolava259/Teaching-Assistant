from typing import Iterable, Type, List, Union, Tuple
from uuid import UUID, uuid4

from applications.workers.bases.BasePort import CrossProcessPortProperty
from applications.workers.abstracts.strategy import AbstractLBStrategy
from applications.workers.implementations.impl_lb_metric import RoundRobinMetric, WeightedRoundRobinMetric, \
    LeastConnectionMetric, WeightedLeastConnectionMetric, IdHashMetric, LeastResponseTimeMetric, RandomMetric, \
    WeightedRandomMetric, MostCapacityMetric

from collections import deque
from typing import Deque as Queue

class RoundRobinLBStrategy(AbstractLBStrategy[CrossProcessPortProperty,RoundRobinMetric, None]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = RoundRobinMetric()
        self.queue: Queue[int] = deque(range(self.num_port))

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]], **kwargs) -> UUID:

        ids: List[UUID] = [self.metric.compute_score(prop)[0] for prop in properties]

        port_no = self.queue.popleft()

        self.queue.append(port_no)

        return ids[port_no]

import heapq

class WeightedRoundRobinLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, WeightedRoundRobinMetric, int]):
    def __init__(self, num_port: int = 32, degenerate_factor:int = 1):
        self.num_port = num_port
        self.metric = WeightedRoundRobinMetric()
        self.pq: List[Tuple[int, UUID]] | None = None
        self.degenerate_factor = degenerate_factor

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:

        if not self.pq or len(self.pq) == 0:
            self.pq = [(sc[1], sc[0]) for sc in [self.metric.compute_score(prop) for prop in properties]]
            heapq.heapify(self.pq)

        weight, port_id = heapq.heappop(self.pq)
        heapq.heappush(self.pq, (weight-self.degenerate_factor, port_id))
        return port_id

class LeastConnectionLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, LeastConnectionMetric, int]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = LeastConnectionMetric()

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:

        scores = [self.metric.compute_score(prop) for prop in properties]

        port_id, num_conn = min(scores, key=lambda c: c[1])

        return port_id


class WeightedLeastConnectionLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, WeightedLeastConnectionMetric, float]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = WeightedLeastConnectionMetric()

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:
        scores = [self.metric.compute_score(prop) for prop in properties]

        port_id, num_conn = min(scores, key=lambda c: c[1])

        return port_id

class IdHashLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, IdHashMetric, None]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = IdHashMetric(num_port=num_port)

    def uuid_hash(self, uuid:UUID) -> int:
        uuid_str = str(uuid)
        hash_val = 0
        for c in uuid_str:
            if c == "-":
                continue
            hash_val += ord('c')

        hash_val %= self.num_port
        return hash_val

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:
        ids = [self.metric.compute_score(prop)[0] for prop in properties]

        return ids[self.uuid_hash(kwargs.get('req_id', uuid4()))]

class LeastResponseTimeLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, LeastResponseTimeMetric, float]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = LeastResponseTimeMetric()

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:
        scores = [self.metric.compute_score(prop) for prop in properties]

        port_id, num_conn = min(scores, key=lambda c: c[1])

        return port_id

import random

class RandomLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, RandomMetric, None]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = RandomMetric()
        self.port_no = list(range(self.num_port))

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:
        ids = [self.metric.compute_score(prop)[0] for prop in properties]

        return random.choice(ids)

from itertools import accumulate
class WeightedRandomLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, WeightedRandomMetric, int]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = WeightedRandomMetric()

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:
        scores = [self.metric.compute_score(prop) for prop in properties]
        weights= [sc[1] for sc in scores]

        total_weight = sum(weights)

        accum_weights = list(accumulate(weights))
        map_id = [0] * total_weight
        counter = accum_weights[0]
        p_id = 0

        for i in range(total_weight):
            if i >= counter:
                p_id += 1
                counter += accum_weights[p_id]
            map_id[i] = p_id

        return scores[random.choice(map_id)][0]

class MostCapacityLBStrategy(AbstractLBStrategy[CrossProcessPortProperty, MostCapacityMetric, int]):
    def __init__(self, num_port: int = 32):
        self.num_port = num_port
        self.metric = LeastConnectionMetric()

    def promote_port(self, properties: Iterable[Union[Type[CrossProcessPortProperty], CrossProcessPortProperty]],
                     **kwargs) -> UUID:

        scores = [self.metric.compute_score(prop) for prop in properties]

        port_id, num_conn = max(scores, key=lambda c: c[1])

        return port_id
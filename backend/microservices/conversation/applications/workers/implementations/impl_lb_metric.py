from uuid import UUID

from applications.workers.abstracts.lb_metric import AbstractPortMetric
from typing import  Tuple
from applications.workers.bases.BasePort import CrossProcessPortProperty

class RoundRobinMetric(AbstractPortMetric[CrossProcessPortProperty, None]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, None]:
        report = prop.get_report()
        return report["id"], None

class WeightedRoundRobinMetric(AbstractPortMetric[CrossProcessPortProperty, int]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, int]:
        report = prop.get_report()
        return report["id"], report["weight"]


class LeastConnectionMetric(AbstractPortMetric[CrossProcessPortProperty, int]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, int]:
        report = prop.get_report()
        return report["id"], report["num_conn"]

class WeightedLeastConnectionMetric(AbstractPortMetric[CrossProcessPortProperty, float]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, float]:
        report = prop.get_report()
        return report["id"], float(report["num_conn"])/float(report["weight"])

class IdHashMetric(AbstractPortMetric[CrossProcessPortProperty, None]):
    def __init__(self, num_port:int = 32):
        self.num_port = num_port
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, None]:
        report = prop.get_report()
        return report["id"], None

class LeastResponseTimeMetric(AbstractPortMetric[CrossProcessPortProperty, float]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, float]:
        report = prop.get_report()
        return report["id"], report["avg_resp_time"]


class RandomMetric(AbstractPortMetric[CrossProcessPortProperty, None]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, None]:
        report = prop.get_report()
        return report["id"], None

class WeightedRandomMetric(AbstractPortMetric[CrossProcessPortProperty, int]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, int]:
        report = prop.get_report()
        return report["id"], report["weight"]

class MostCapacityMetric(AbstractPortMetric[CrossProcessPortProperty, int]):
    def compute_score(self, prop: CrossProcessPortProperty) -> Tuple[UUID, int]:
        report = prop.get_report()
        return report["id"], report["capacity"] - report["num_msg"]
from interfaces.async_pub_sub.generic_types import TEvent, TTransformedResult, TPrimitiveResult
from typing import Generic, Optional, Union
from dataclasses import dataclass, field
import threading
import os


@dataclass
class EventWrapper(Generic[TEvent]):


    event: Optional[TEvent] = field(default = None)

    pid: int = field(default=-1)
    ppid: int = field(default=-1)

    tid: int = field(default=-1)
    tname: str = field(default="")

    route: Optional[str] = field(default="")
    information: Optional[str] = field(default=None)

    def __init__(self, event: TEvent, route: str | None = None, information: str | None = None):
        self.event = event
        self.pid = os.getpid()
        self.ppid = os.getppid()

        self.tid = threading.get_ident()
        self.tname = threading.current_thread().name

        self.route = route

        self.information = information

    @property
    def value(self) -> TEvent:
        return self.event





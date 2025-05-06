import datetime
from enum import IntEnum
from typing import Annotated, Optional, Union
from abc import ABC
from uuid import UUID, uuid4
from dataclasses import field, dataclass
from datetime import date

@dataclass
class BaseEntity(ABC):
    created_date: date
    updated_date: date
    id: UUID = field(default_factory=uuid4)

class State(IntEnum):
    NoAction = 3
    Added = 0
    Deleted = 1
    Updated = 2
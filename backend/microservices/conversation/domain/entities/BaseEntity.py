import datetime
from typing import Annotated, Optional, Union
from abc import ABC
from uuid import UUID, uuid4
from dataclasses import field, dataclass
from datetime import date

@dataclass
class BaseEntity(ABC):

    created_date: date
    updated_date: date
    deleted: bool = field(default = False)
    id: UUID = field(default_factory=uuid4)
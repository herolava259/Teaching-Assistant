from enum import StrEnum
from typing import List, Optional, Union, Any, Literal
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4


class FileType(StrEnum):
    pdf = 'pdf'
    txt = "txt"
    doc = 'doc'
    png = 'png'


@dataclass
class DocumentMetadata:
    file_name: str
    created_at: date
    type: FileType
    size: int
    object_id: UUID
    role_permissions: str
    state: Literal['created', 'deleted']
    id: UUID = field(default_factory=uuid4)


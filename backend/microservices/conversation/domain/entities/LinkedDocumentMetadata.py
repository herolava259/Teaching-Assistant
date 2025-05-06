from enum import StrEnum
from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4
from BaseEntity import State

class FileType(StrEnum):
    pdf = 'pdf'
    txt = "txt"
    doc = 'doc'
    png = 'png'

@dataclass
class LinkedDocumentMetadata:
    file_name: str
    created_at: date
    type: FileType
    size: int
    object_id: UUID
    role_permissions: str
    created_user_id: UUID
    message_id: UUID
    state: State = field(default=State.Added)
    id: UUID = field(default_factory=uuid4)


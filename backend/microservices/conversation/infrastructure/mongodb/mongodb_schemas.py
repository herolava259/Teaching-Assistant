from mongoengine import Document, EmbeddedDocument, fields, connect
from utils.configuration import Configuration
from datetime import date
from uuid import UUID
from typing import Optional, List
from domain.entities.BaseEntity import State
from domain.entities.LinkedDocumentMetadata import FileType

#connect(Configuration.load('database_connections:mongodb:default'))

class FeedbackDataModel(EmbeddedDocument):
    rating: int = fields.IntField(required=True)
    content: str = fields.StringField(required=True, default='There are positive feedback')

class DocumentMetadataModel(EmbeddedDocument):
    file_name: str = fields.StringField(required=True)
    created_at: date = fields.DateTimeField(required=True)
    file_type: FileType = fields.EnumField(FileType)
    file_size: int = fields.IntField(min_value=0, required=True)
    object_id: UUID = fields.UUIDField(required=True)
    role_permissions: str = fields.StringField(required=True, default='admin')
    created_user_id: UUID = fields.UUIDField(required=True)
    msg_id: UUID = fields.UUIDField(required=True)
    state: State = fields.EnumField(State)
    id: UUID = fields.UUIDField(required=True)


class MessageDataModel(EmbeddedDocument):
    conversation_id: UUID = fields.UUIDField(required=True)
    chunk_id: UUID = fields.UUIDField(required=True)
    reference_msg_id: UUID = fields.UUIDField()
    created_at: date = fields.DateTimeField(required=True)
    updated_at: date = fields.DateTimeField(required=True)
    feedback: Optional[FeedbackDataModel] = fields.EmbeddedDocumentField(FeedbackDataModel)
    state: State = fields.EnumField(State)
    no_of_msg: int = fields.IntField(0, 10000)
    documents: List[DocumentMetadataModel] = fields.EmbeddedDocumentListField(DocumentMetadataModel)
    id: UUID = fields.UUIDField(required=True)



class MessageChunkDataModel(Document):
    conversation_id: UUID = fields.UUIDField(required=True)
    created_at: date = fields.DateTimeField(required=True)
    no_of_chunk: int = fields.IntField(min_value=0)
    limit_length: int = fields.IntField(min_value=10, max_value=20)
    messages: List[MessageDataModel] = fields.EmbeddedDocumentListField(MessageDataModel)
    length: int = fields.IntField(min_value=1)
    id: UUID = fields.UUIDField(required=True)






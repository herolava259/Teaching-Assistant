from mongoengine import Document, EmbeddedDocument, fields, connect
from utils.configuration import Configuration


connect(Configuration.load('database_connections:mongodb:default'))


class ConversationDataModel(EmbeddedDocument):
    pass

class MessageChunkDataModel(Document):
    pass


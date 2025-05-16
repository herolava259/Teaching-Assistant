from typing import Optional, Any, List
from sqlalchemy.dialects.postgresql import UUID
from domain.aggregates.Conversation import Conversation
from interfaces.repositories.conversation_repository import IConversationRepository
from utils.configuration import Configuration

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..schema import ConversationRecord


class ConversationRepository(IConversationRepository):

    @staticmethod
    def __init_session():
        conn_string = Configuration.load('database_connections:postgresql:default')
        engine = create_engine(conn_string)
        return sessionmaker(bind=engine)()


    def __init__(self, ):
        pass
    async def modify(self, cons: Conversation) -> bool:
        pass

    async def safety_update(self, cons: Conversation, params: List[str] | None) -> bool:
        pass

    async def update(self, cons: Conversation) -> bool:
        pass

    async def get(self, **filters: Any) -> Optional[Conversation]:
        with ConversationRepository.__init_session() as session:
            record = session.query(ConversationRecord).filter(**filters).first()
            return record

    async def get_by_id(self, ids: UUID) -> Optional[Conversation]:
        with ConversationRepository.__init_session() as session:
            record = session.query(ConversationRecord).filter(ids == ConversationRecord.id).first()
            return record
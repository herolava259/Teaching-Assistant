import datetime
from typing import Optional, Any, List, Union, Dict
from sqlalchemy.dialects.postgresql import UUID
from domain.aggregates.Conversation import Conversation
from domain.entities.BaseEntity import State
from interfaces.repositories.conversation_repository import IConversationRepository
from utils.configuration import Configuration
from ..mappers.conversation import ConversationMapper

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..schema import ConversationRecord, object_to_dict

from sqlalchemy import insert, exists, update
import uuid


class ConversationRepository(IConversationRepository):

    @staticmethod
    def __init_session():
        conn_string = Configuration.load('database_connections:postgresql:default')
        engine = create_engine(conn_string)
        return sessionmaker(bind=engine)()

    @staticmethod
    def __create_engine():
        conn_string = Configuration.load('database_connections:postgresql:default')
        engine = create_engine(conn_string)
        return engine

    def __init__(self, ):
        pass

    async def add(self, entity: Conversation) -> Optional[UUID]:
        with ConversationRepository.__init_session() as session:
            if not entity.id:
                entity.id = uuid.uuid4()
            record = ConversationMapper.entity_to_db(entity)
            session.add(record)
            session.commit()
        return entity.id

    @staticmethod
    async def __exist_entity(idx: UUID) -> bool:
        with ConversationRepository.__init_session() as session:
            stmt = session.query(exists().where(idx == ConversationRecord.id)).scalar()
            return stmt

    async def modify(self, cons: Conversation) -> bool:
        state = cons.state
        if state != State.Added and await ConversationRepository.__exist_entity(cons.id):
            return False
        if state == State.NoAction:
            return True
        elif state == State.Updated:
            return await self.update(cons)
        elif state == State.Deleted:
            return await self.remove(cons)
        elif state == State.Added:
            return (await self.add(cons)) is not None

        return False


    async def safety_update(self, cons: Conversation, params: List[str] | None) -> bool:
        pass

    async def update(self, obj: Union[Conversation, Dict[str, Any]]) -> bool:
        if (isinstance(obj, Conversation)
                and (not obj.id or not await ConversationRepository.__exist_entity(obj.id))):
            return False
        if isinstance(obj, dict) and not obj.get('id', None):
            return False
        now = datetime.datetime.now()

        async def update_by_entity(entity: Conversation) -> bool:
            entity.updated_at = now
            with ConversationRepository.__init_session() as session:
                json_obj = object_to_dict(ConversationMapper.entity_to_db(entity))
                session.query(ConversationRecord).filter_by(id=json_obj.pop('id')).update(json_obj)
                session.commit()
            return True

        async def update_by_params(params: Dict[str, id]) -> bool:
            params['updated_date'] = now
            engine = ConversationRepository.__create_engine()
            idx = params.pop('id')
            stmt = (update(ConversationRecord)
                    .where(idx==ConversationRecord.id)
                    .values(**params))

            with engine.begin() as conn:
                conn.excute(stmt)
                conn.commit()
            return True

        if isinstance(obj, Conversation):
            return await update_by_entity(obj)
        elif isinstance(obj, dict):
            return await update_by_params(obj)

        return False


    async def total_conversation_of(self, user_id: UUID) -> int:
        pass

    async def get(self, **filters: Any) -> Optional[Conversation]:
        with ConversationRepository.__init_session() as session:
            record: Optional[ConversationRecord] = session.query(ConversationRecord).filter(**filters).first()
            if not record:
                return None
            entity = ConversationMapper.db_to_entity(record)
            return entity

    async def get_by_id(self, ids: UUID) -> Optional[Conversation]:
        with ConversationRepository.__init_session() as session:
            record: Optional[ConversationRecord] = session.query(ConversationRecord).filter(ids == ConversationRecord.id).first()
            if not record:
                return None
            entity = ConversationMapper.db_to_entity(record)
            return entity

    async def remove(self, obj: Union[UUID, Conversation]) -> bool:

        async def remove_by_entity(entity: Conversation) -> bool:
            with ConversationRepository.__init_session() as session:
                record = ConversationMapper.entity_to_db(entity)
                session.delete(record)
                session.commit()
            return True

        async def remove_by_id(idx: UUID)-> bool:
            with ConversationRepository.__init_session() as session:
                record = session.query(ConversationRecord).filter_by(id=idx).first()
                if record is None:
                    return False
                session.delete(record)
                session.commit()
            return True

        if isinstance(obj, UUID):
            return await remove_by_id(obj)
        if isinstance(obj, Conversation):
            return await remove_by_entity(obj)
        return False

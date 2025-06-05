import datetime
from typing import Optional, Any, List, Union, Dict
from sqlalchemy.dialects.postgresql import UUID
from domain.aggregates.Conversation import Conversation
from domain.aggregates.Pagination import PaginationParams, PaginationDataCollection
from domain.entities.BaseEntity import State
from interfaces.repositories.conversation_repository import IConversationRepository
from utils.configuration import Configuration
from ..mappers.conversation import ConversationMapper as mapper, conversation_mapping_fields

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..schema import ConversationRecord, object_to_dict

from sqlalchemy import insert, exists, update
import uuid
from sqlalchemy.orm import Query
from copy import deepcopy


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
            record = mapper.entity_to_db(entity)
            session.add(record)
            session.commit()
        return entity.id

    @staticmethod
    async def __exist_entity(idx: UUID) -> bool:
        with ConversationRepository.__init_session() as session:
            existed = session.query(exists().where(idx == ConversationRecord.id)).scalar()
            return existed

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
    async def pagination_query(self, pagination_params: PaginationParams[Conversation]) -> PaginationDataCollection[
        Conversation]:
        from sqlalchemy import and_, or_
        from domain.aggregates.Pagination import ConditionBetweenType, OperationType, OrderType
        def gen_conditional_expr(field_name: str, operator: OperationType, value: Any):
            col_term = getattr(ConversationRecord, field_name)
            if operator == OperationType.LessThan:
                return col_term < value
            elif operator == OperationType.LessThanOrEqual:
                return col_term <= value
            elif operator == OperationType.GreaterThan:
                return col_term > value
            elif operator == OperationType.GreaterThanOrEqual:
                return col_term >= value
            elif operator == OperationType.Like:
                return col_term.like(value)
            elif operator == OperationType.Equal:
                return col_term == value
            return operator == value
        def build_conditional_query(query: Query) -> Query:
            conditional_params = pagination_params.filter_params
            table_value_params = [deepcopy(filter_param) for filter_param in conditional_params]
            for filter_param in table_value_params:
                col_name = conversation_mapping_fields[filter_param.field_name]
                cond_between = and_ if filter_param.condition_between == ConditionBetweenType.And else or_
                query = query.filter(
                    cond_between(tuple(
                        gen_conditional_expr(col_name, filter_cond.operator, filter_cond.value)
                        for filter_cond in filter_param.filter_conditions)))

            return query
        def build_order_by_clauses(query: Query) -> Query:
            order_by_clauses = pagination_params.order_by_clauses
            asc_type = order_by_clauses.order_type == OrderType.Ascending

            attributes = [getattr(ConversationRecord, conversation_mapping_fields[field_name]) for field_name in order_by_clauses.order_by_fields]
            return query.order_by(tuple(column_delegate.asc() if asc_type else column_delegate.desc() for column_delegate in attributes))

        with ConversationRepository.__init_session() as session:
            initial_query = session.query(ConversationRecord)
            cond_query = build_conditional_query(initial_query)

            total_record = cond_query.count()
            if total_record == 0:
                return PaginationDataCollection.EmptyDataCollection(page_size = pagination_params.page_size)
            ordered_query = build_order_by_clauses(cond_query)

            total_skip = pagination_params.page_size * (pagination_params.page_num-1)
            total_take = pagination_params.page_size
            pagination_query = ordered_query.offset(total_skip).limit(total_take)

            records = pagination_query.all()
            data_collection = PaginationDataCollection[Conversation].EmptyDataCollection()

            data_collection.page_num = pagination_params.page_num
            data_collection.page_size = pagination_params.page_size
            data_collection.total_record = total_record
            data_collection.data = [mapper.db_to_entity(record) for record in records]
        return data_collection
    async def safety_update(self, cons: Conversation, params: List[str] | None) -> bool:

        exclude_fields = {'id'}
        include_fields = {"updated_date"}
        updated_fields = set(params) & include_fields - exclude_fields
        if updated_fields.difference(set(cons.__dict__.keys())):
            raise RuntimeError("Argument 'params' have invalid field. Some param name in params are not fields in Conversation entity")

        inverse_mapping_fields = {val: key for key, val in conversation_mapping_fields.items()}
        field_values = cons.__dict__
        modify_value_mapping: Dict[str, Any] = {inverse_mapping_fields[field]: field_values[field] for field in updated_fields}

        ids = cons.id
        result = False
        modify_value_mapping["updated_date"] = datetime.datetime.now()
        session = ConversationRepository.__init_session()
        try:
            stmt = (update(ConversationRecord)
                    .where(ConversationRecord.id == ids)
                    .values(**modify_value_mapping))
            result = session.execute(stmt)
            session.commit()
        except Exception as ex:
            print(f"Error while execute safety_update from database side. Ex = {ex}")
            session.rollback()
        finally:
            session.close()
        return result == 1

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
                json_obj = object_to_dict(mapper.entity_to_db(entity))
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
        total_record = 0
        from sqlalchemy import func
        with ConversationRepository.__init_session() as session:
            total_record = session.query(func.count(ConversationRecord.id)).filter(ConversationRecord.created_user_id == user_id).scalar()
        return total_record

    async def get(self, **filters: Any) -> Optional[Conversation]:
        with ConversationRepository.__init_session() as session:
            record: Optional[ConversationRecord] = session.query(ConversationRecord).filter(**filters).first()
            if not record:
                return None
            entity = mapper.db_to_entity(record)
            return entity

    async def get_by_id(self, ids: UUID) -> Optional[Conversation]:
        with ConversationRepository.__init_session() as session:
            record: Optional[ConversationRecord] = session.query(ConversationRecord).filter(ids == ConversationRecord.id).first()
            if not record:
                return None
            entity = mapper.db_to_entity(record)
            return entity

    async def remove(self, obj: Union[UUID, Conversation]) -> bool:

        async def remove_by_entity(entity: Conversation) -> bool:
            with ConversationRepository.__init_session() as session:
                record = mapper.entity_to_db(entity)
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

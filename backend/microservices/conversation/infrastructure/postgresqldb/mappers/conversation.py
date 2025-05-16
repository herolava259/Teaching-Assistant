from domain.aggregates.Conversation import Conversation
from ..schema import ConversationRecord
from domain.entities.BaseEntity import State

class ConversationMapper:

    @staticmethod
    def entity_to_db(entity: Conversation) -> ConversationRecord:
        return ConversationRecord(id=entity.id,
                                  title=entity.title,
                                  counter_chunk=entity.counter_chunk,
                                  created_date=entity.created_at,
                                  updated_date=entity.updated_at,
                                  created_user_id=entity.created_user_id,
                                  limit_invitation=entity.limit_invitation,
                                  deleted=entity.deleted)
    @staticmethod
    def db_to_entity(record: ConversationRecord) -> Conversation:

        return Conversation(created_at=record.created_date,
                            updated_at=record.updated_date,
                            created_user_id=record.created_user_id,
                            limit_invitation=record.limit_invitation,
                            deleted=record.deleted,
                            state=State.NoAction,
                            title=record.title,
                            counter_chunk=record.counter_chunk,
                            id=record.id)
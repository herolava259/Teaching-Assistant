from ..commands import conversation_commands as command
from domain.aggregates.Conversation import Conversation
from ..responses.conversation_response import *
import datetime
class ConversationMapper:
    @staticmethod
    def map_to_entity_response(domain_obj: Conversation | None) -> ConversationEntityResponse:

        response = ConversationEntityResponse(response_created_time=datetime.datetime.now(),
                                              status= ResponseStatus.Success if not domain_obj else ResponseStatus.Error,
                                              entity= domain_obj,
                                              entity_id= domain_obj.id if domain_obj else None)


        return response



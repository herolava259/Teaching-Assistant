from abc import ABC, abstractmethod
from adapters.base_requests import ConversationBaseRequest
from adapters.responses.conversation_response import ConversationBaseResponse
from interfaces.repositories.conversation_repository import IConversationRepository
from adapters.queries.conversation import ConversationGetByIdQuery
from adapters.responses.conversation_response import ConversationEntityResponse
from typing import Dict, Self
from typing import Optional
from adapters.mappers.conversation import ConversationMapper
class AbstractConversationHandler(ABC):

    @abstractmethod
    async def handle(self, request: ConversationBaseRequest) -> ConversationBaseResponse:
        pass


class ConversationGetByIdQueryHandler(AbstractConversationHandler):
    async def handle(self, request: ConversationGetByIdQuery) -> Optional[ConversationEntityResponse]:
        conversation = await self.repo.get_by_id(request.id)
        response = ConversationMapper.map_to_entity_response(conversation)
        return response

    def __init__(self, repo: IConversationRepository):
        self.repo: IConversationRepository = repo



class ConversationPaginationQueryHandler(AbstractConversationHandler):
    async def handle(self, request: ConversationBaseRequest) -> ConversationBaseResponse:
        pass


class ConversationAddCommandHandler(AbstractConversationHandler):
    async def handle(self, request: ConversationBaseRequest) -> ConversationBaseResponse:
        pass
from abc import ABC, abstractmethod
from adapters.base_requests import ConversationBaseRequest
from adapters.responses.conversation_response import ConversationBaseResponse
from interfaces.repositories.conversation_repository import IConversationRepository
from adapters.queries.conversation import ConversationGetByIdQuery, ConversationPaginationQuery
from adapters.responses.conversation_response import ConversationEntityResponse, ConversationPaginationResponse
from typing import Optional, Generic, TypeVar
from adapters.mappers.conversation import ConversationMapper

TRequest = TypeVar('TRequest', bound=ConversationBaseRequest)
TResponse = TypeVar('TResponse', bound=ConversationBaseResponse)
class AbstractConversationHandler(ABC, Generic[TRequest, TResponse]):

    @abstractmethod
    async def handle(self, request: TRequest) -> TResponse:
        pass


class ConversationGetByIdQueryHandler(AbstractConversationHandler[ConversationGetByIdQuery, ConversationEntityResponse]):
    async def handle(self, request: ConversationGetByIdQuery) -> Optional[ConversationEntityResponse]:
        conversation = await self.repo.get_by_id(request.id)
        response = ConversationMapper.map_to_entity_response(conversation)
        return response

    def __init__(self, repo: IConversationRepository):
        self.repo: IConversationRepository = repo



class ConversationPaginationQueryHandler(AbstractConversationHandler[ConversationPaginationQuery,ConversationPaginationResponse]):
    async def handle(self, request: ConversationPaginationQuery) -> ConversationPaginationResponse:
        return await self.repo

    def __init__(self, repo: IConversationRepository):
        self.repo = repo



class ConversationAddCommandHandler(AbstractConversationHandler):
    async def handle(self, request: ConversationBaseRequest) -> ConversationBaseResponse:
        pass
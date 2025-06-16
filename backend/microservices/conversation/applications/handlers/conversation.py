from abc import ABC, abstractmethod
from adapters.base_requests import ConversationBaseRequest
from adapters.responses.conversation_response import ConversationBaseResponse, ConversationSingularResponse, \
    ConversationSignalResponse
from interfaces.repositories.conversation_repository import IConversationRepository
from adapters.queries.conversation import ConversationGetByIdQuery, ConversationPaginationQuery
from adapters.responses.conversation_response import ConversationEntityResponse, ConversationPaginationResponse
from typing import Optional, Generic, TypeVar
from adapters.mappers.conversation import ConversationMapper
from domain.aggregates.Conversation import Conversation
from adapters.commands.conversation_commands import ConversationCreateCommand, ConversationUpdateCommand
from uuid import UUID
from adapters.responses.conversation_response import ResponseStatus

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
        params = ConversationMapper.pagination_out_to_in(request)
        data_collection = await self.repo.pagination_query(params)

        return ConversationMapper.pagination_in_to_out(data_collection)

    def __init__(self, repo: IConversationRepository):
        self.repo = repo



class ConversationAddCommandHandler(AbstractConversationHandler[ConversationCreateCommand, ConversationSingularResponse[UUID]]):
    def __init__(self, repo: IConversationRepository):
        self.repo = repo
    async def handle(self, request: ConversationCreateCommand) -> ConversationSingularResponse[UUID]:
        conversation: Conversation = ConversationMapper.create_cmd_to_entity(request)
        result : UUID | None = await self.repo.add(conversation)

        if not result:
            return ConversationSingularResponse[UUID](status=ResponseStatus.Error, entity_id=None)

        return ConversationSingularResponse[UUID](entity_id=result)

class ConversationUpdateCommandHandler(AbstractConversationHandler[ConversationUpdateCommand, ConversationSignalResponse]):
    async def handle(self, request: ConversationUpdateCommand) -> ConversationSignalResponse:
        pass
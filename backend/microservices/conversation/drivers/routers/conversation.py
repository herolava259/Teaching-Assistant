from fastapi import APIRouter, status
from uuid import UUID
from adapters.queries.conversation import ConversationPaginationQuery
from adapters.commands.conversation_commands import ConversationCreateCommand

router = APIRouter(
    prefix="/conversation/conversation_spec/",
    tags = ["items"],
    dependencies = [],
    responses={404: {"description": "Not found"}}
)


from ..dependencies.conversation import create_mediator
from adapters.queries.conversation import ConversationGetByIdQuery
from adapters.responses.conversation_response import ConversationEntityResponse, ConversationPaginationResponse
conversation_mediator = create_mediator()

@router.get("conversation_single_get/{conversation_id}",
            status_code=status.HTTP_204_NO_CONTENT,
            response_model=ConversationEntityResponse)
async def get_conversation_by_id(conversation_id: UUID):
    query = ConversationGetByIdQuery(conversation_id=conversation_id)

    response = await conversation_mediator.send(query)

    return response


@router.post(path="conversation_pagination_query/{conversation_id}",
             status_code=status.HTTP_302_FOUND,
             response_model=ConversationPaginationResponse)
async def pagination_query(page_query: ConversationPaginationQuery):
    return await conversation_mediator.send(page_query)


@router.post("conversation_create/")
async def create_conversation(create_command: ConversationCreateCommand):
    return await conversation_mediator.send(create_command)




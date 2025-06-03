from fastapi import APIRouter, status
from uuid import UUID

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
async def pagination_query():
    pass


@router.post("conversation_create/")
async def create_conversation():
    pass




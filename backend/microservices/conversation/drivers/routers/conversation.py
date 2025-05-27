from fastapi import APIRouter, status
from uuid import UUID

router = APIRouter(
    prefix="/conversation/conversation_spec/",
    tags = ["items"],
    dependencies = [],
    responses={404: {"description": "Not found"}}
)


@router.get("{conversation_id}",
            status_code=status.HTTP_204_NO_CONTENT)
async def get_conversation_by_id(conversation_id: UUID):
    pass

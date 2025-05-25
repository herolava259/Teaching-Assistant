from langgraph.store.memory import InMemoryStore
from langgraph.store.base import IndexConfig



def build_in_memory_store_for_graph(embedding_model: str = "openai:text-embedding-3-small") -> InMemoryStore:
    return InMemoryStore(index=IndexConfig(embed=embedding_model))

from langmem import create_manage_memory_tool, create_search_memory_tool

def build_manage_memory_tool():
    return create_manage_memory_tool(namespace=(
        "email_assistant",
        "{langgraph_user_id}",
        "collection"
    ))

def build_search_memory_tool():
    return create_search_memory_tool(
    namespace=(
        "email_assistant",
        "{langgraph_user_id}",
        "collection"
    )
)
from llama_index.core import SimpleDirectoryReader
from llama_index.core import Document
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, ServiceContext
from llama_index.embeddings.openai import OpenAIEmbedding

def build_simple_doc_rag(file_path: str, api_key:str, model_name: str) -> BaseQueryEngine:
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()

    document = Document(text='\n\n'.join(doc.text for doc in documents))

    llm = OpenAI(model=model_name, api_key=api_key, temperature=0.1)
    embed_model = OpenAIEmbedding()
    service_context = ServiceContext.from_defaults(llm = llm, embed_model=embed_model)
    index = VectorStoreIndex.from_documents([document],
                                            service_context = service_context)

    query_engine = index.as_query_engine()

    return query_engine







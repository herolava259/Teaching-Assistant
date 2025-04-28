from llama_index.core import ServiceContext, VectorStoreIndex, StorageContext
from llama_index.core.node_parser import SentenceWindowNodeParser
from llama_index.core.postprocessor import MetadataReplacementPostProcessor
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core import load_index_from_storage
import os
from llama_index.embeddings.openai import OpenAIEmbedding
def build_sentence_window_index(
        document,
        llm,
        embed_model: str | None = 'local:BAAI/bge-small-en-v1.5',
        save_dir = 'sentence_index'
):
    node_parser = SentenceWindowNodeParser.from_defaults(
        window_size=3,
        window_metadata_key='window',
        original_text_metadata_key='original_text'
    )
    if not embed_model:
        embed_model = OpenAIEmbedding()

    sentence_context = ServiceContext.from_defaults(
        llm = llm,
        embed_model = embed_model,
        node_parser = node_parser
    )

    if not os.path.exists(save_dir):
        sentence_index = VectorStoreIndex.from_documents(
            [document],
            service_context=sentence_context
        )
        sentence_index.storage_context.persist(persist_dir = save_dir)
    else:
        sentence_index = load_index_from_storage(
            StorageContext.from_defaults(persist_dir=save_dir),
            service_context=sentence_context
        )

    return sentence_index

def get_sentence_window_query_engine(
    sentence_index,
    similarity_top_k=6,
    rerank_top_n=2
):
    post_proccessor = MetadataReplacementPostProcessor(target_metadata_key='window')

    rerank = SentenceTransformerRerank(top_n=rerank_top_n,
                                       model ='BAAI/bge-reranker-base')

    sentence_window_engine = sentence_index.as_query_engine(
        similarity_top_k=similarity_top_k,
        node_processosrs = [post_proccessor, rerank]
    )

    return sentence_window_engine

from trulens_eval import (
    Feedback,
    TruLlama,
    OpenAI,
)
from trulens.apps.llamaindex import TruLlama
import numpy as np

from typing import Tuple

def gen_evaluation_metrics(api_key: str, model_name: str, query_engine) -> Tuple[Feedback, Feedback, Feedback]:
    provider = OpenAI(api_key=api_key, model_name = model_name)

    context = TruLlama.select_context(query_engine)

    f_groundedness = (
        Feedback(
            provider.groundedness_measure_with_cot_reasons, name= 'Groundedness'
        )
        .on(context.collect())
        .on_output()
    )

    f_answer_relevance = Feedback(
        provider.relevance_with_cot_reasons, name='Answer Relevance'
    ).on_input_output()

    f_context_relevance = (
        Feedback(
            provider.context_relevance_with_cot_reasons, name='Context Relevance'
        ).on_input()
        .on(context)
        .aggregate(np.mean)
    )

    return f_groundedness, f_answer_relevance, f_context_relevance


def build_trulens_recorder(query_engine, app_id, api_key, model_name) -> TruLlama:

    feedbacks = gen_evaluation_metrics(api_key, model_name, query_engine)

    return TruLlama(query_engine, app_id = app_id, feedbacks=feedbacks)










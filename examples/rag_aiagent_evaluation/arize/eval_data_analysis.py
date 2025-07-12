import phoenix as px
import os
import json
from phoenix.evals import (
    TOOL_CALLING_PROMPT_TEMPLATE,
    llm_classify,
    OpenAIModel
)

from phoenix.trace import SpanEvaluations
from phoenix.trace.dsl import SpanQuery
from openinference.instrumentation import suppress_tracing
from example_agent.external_tools import tools_schema
from example_agent.setup_tracing import PROJECT_NAME
from example_agent.prompts import CLARITY_LLM_JUDGE_PROMPT


def query_data_analysis(span_kind: str = 'AGENT', response: str = 'output.value', query= 'input.value'):

    query = SpanQuery().where(f"span_kind=='{span_kind}'").select(response=response, query=query)

    clarity_df = px.Client().query_spans(query, project_name=PROJECT_NAME, timeout=None)

    return clarity_df


def apply_clarity_classify(clarity_df):
    with suppress_tracing():
        clarity_eval = llm_classify(
            dataframe = clarity_df,
            template = CLARITY_LLM_JUDGE_PROMPT,
            rails = ['clear', 'unclear'],
            model = OpenAIModel(model='gpt-4o'),
            provide_explanation = True
        )

    clarity_eval['score'] = clarity_eval.apply(lambda x: 1 if x['label'] == 'clear' else 0, axis =1)

    return clarity_eval


def eval_clarity():
    clarity_df = query_data_analysis()
    clarity_df = apply_clarity_classify(clarity_df)
    return clarity_df

def running_clarity_eval():
    clarity_df = eval_clarity()

    px.Client().log_evaluations(SpanEvaluations(eval_name= "Response Clarity", dataframe=clarity_df))

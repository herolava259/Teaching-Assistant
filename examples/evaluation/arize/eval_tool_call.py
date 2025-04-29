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
from examples.evaluation.arize.example_agent.setup_tracing import PROJECT_NAME


def query_tool_call_span(where_cond: str = "span_kind == 'LLM'", quest: str = 'input.value', tool_call: str = 'llm.tools'):

    query = SpanQuery().where(where_cond).select(question=quest, tool_call = tool_call)

    tool_calls_df = px.Client().query_spans(query, project_name=PROJECT_NAME, timeout=None)

    tool_calls_df = tool_calls_df.dropna(subset=['tool_call'])

    return tool_calls_df


def eval_tool_call():
    with suppress_tracing():
        tool_call_df = query_tool_call_span()
        tool_call_eval = llm_classify(
            dataframe = tool_call_df,
            template = TOOL_CALLING_PROMPT_TEMPLATE.template[0].template.replace("{tool_definitions}",
                                                                 json.dumps(tools_schema).replace("{", '"').replace("}", '"')),
            rails = ['correct', 'incorrect'],
            model = OpenAIModel(model = 'gpt-4o'),
            provide_explanation = True
        )

    tool_call_df['score'] = tool_call_df.apply(lambda x: 1 if x['label'] == 'correct' else 0, axis=1)

    return tool_call_df


def running_tool_call_eval():
    tool_call_eval = eval_tool_call()

    px.Client().log_evaluations(
        SpanEvaluations(eval_name= 'Tool Calling Eval', dataframe=tool_call_eval)
    )
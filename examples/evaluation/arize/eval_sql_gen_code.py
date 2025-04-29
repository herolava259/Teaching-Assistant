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
from example_agent.prompts import SQL_EVAL_GEN_PROMPT


def query_sql_code_gen(span_kind: str = 'LLM', query_gen='llm.output_messages', question='input.value'):

    query = SpanQuery().where(f"span_kind=='{span_kind}'").select(query_gen=query_gen, question=question)

    sql_df = px.Client().query_spans(query, project_name=PROJECT_NAME, timeout=None)

    prefix_template = 'Generate an SQL query based on a prompt'
    sql_df = sql_df[sql_df['question'].str.contains(prefix_template, na=False)]

    return sql_df

def apply_classify_correct(sql_stats_df):

    with suppress_tracing():
        sql_gen_eval = llm_classify(
            dataframe = sql_stats_df,
            template = SQL_EVAL_GEN_PROMPT,
            rails = ['correct', 'incorrect'],
            model = OpenAIModel(model="gpt-4o"),
            provide_explanation= True
        )

    sql_gen_eval['score'] = sql_gen_eval.apply(lambda x: 1 if x['label'] == 'correct' else 0, axis=1)

    return sql_gen_eval

def running_sql_gen_eval():
    sql_df = query_sql_code_gen()
    sql_df = apply_classify_correct(sql_df)

    px.Client().log_evaluations(
        SpanEvaluations(eval_name='SQL Gen Eval', dataframe=sql_df)
    )


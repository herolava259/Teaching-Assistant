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


def query_code_gen(name: str = 'generate_visualization', generated_code='output.value'):

    query = SpanQuery().where(f"name == '{name}'").select(generated_code=generated_code)

    code_gen_df = px.Client().query_spans(query,
                                          project_name = PROJECT_NAME,
                                          timeout=None)
    return code_gen_df

def code_is_runnable(output: str) -> bool:
    """Check if the code is runnable"""

    output = output.strip()
    output = output.replace("```python", "").replace("```", "")
    try:
        exec(output)
        return True
    except Exception as ex:
        return False

def apply_code_runnable(code_gen_df):
    code_gen_df['label'] = code_gen_df['generated_code'].apply(code_is_runnable).map({True: 'runnable', False: 'not_runnable'})
    code_gen_df['score'] = code_gen_df['label'].map({'runnable': 1.0, 'not_runnable': 0.0})

    return code_gen_df

def eval_code_gen():
    code_gen_df = query_code_gen()
    code_gen_df = apply_code_runnable(code_gen_df)

    return code_gen_df

def running_code_gen_eval():
    code_gen_eval = eval_code_gen()

    px.Client().log_evaluations(eval_name='Runnable Code Eval', dataframe=code_gen_eval)

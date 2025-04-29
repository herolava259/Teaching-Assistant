import phoenix as px
from phoenix.evals import OpenAIModel, llm_classify, TOOL_CALLING_PROMPT_TEMPLATE
from phoenix.experiments import run_experiment, evaluate_experiment
from phoenix.experiments.types import Example
from phoenix.experiments.evaluators import create_evaluator

from phoenix.otel import register
import pandas as pd
from example_agent.ExampleAgent import ExampleAgent
from example_agent.external_tools import tools_schema
from utils import process_messages, get_phoenix_endpoint

from datetime import datetime
import json
import os

from evaluate_prompts import CLARITY_LLM_JUDGE_PROMPT, ENTITY_CORRECTNESS_LLM_JUDGE_PROMPT

from utils import get_openai_api_key

from typing import List

overall_experiment_questions = [
    {'question': 'What was the most popular product SKU?',
     'sql_result': '   SKU_Coded  Total_Qty_Sold 0    6200700         52262.0',
     'sql_generated': '```sql\nSELECT SKU_Coded, SUM(Qty_Sold) AS Total_Qty_Sold\nFROM sales\nGROUP BY SKU_Coded\nORDER BY Total_Qty_Sold DESC\nLIMIT 1;\n```'},
    {'question': 'What was the total revenue across all stores?',
     'sql_result': '   Total_Revenue 0   1.327264e+07',
     'sql_generated': '```sql\nSELECT SUM(Total_Sale_Value) AS Total_Revenue\nFROM sales;\n```'},
    {'question': 'Which store had the highest sales volume?',
     'sql_result': '   Store_Number  Total_Sales_Volume 0          2970             59322.0',
     'sql_generated': '```sql\nSELECT Store_Number, SUM(Total_Sale_Value) AS Total_Sales_Volume\nFROM sales\nGROUP BY Store_Number\nORDER BY Total_Sales_Volume DESC\nLIMIT 1;\n```'},
    {'question': 'Create a bar chart showing total sales by store',
     'sql_result': '    Store_Number    Total_Sales 0            880  420302.088397 1           1650  580443.007953 2           4180  272208.118542 3            550  229727.498752 4           1100  497509.528013 5           3300  619660.167018 6           3190  335035.018792 7           2970  836341.327191 8           3740  359729.808228 9           2530  324046.518720 10          4400   95745.620250 11          1210  508393.767785 12           330  370503.687331 13          2750  453664.808068 14          1980  242290.828499 15          1760  350747.617798 16          3410  410567.848126 17           990  378433.018639 18          4730  239711.708869 19          4070  322307.968330 20          3080  495458.238811 21          2090  309996.247965 22          1320  592832.067579 23          2640  308990.318559 24          1540  427777.427815 25          4840  389056.668316 26          2860  132320.519487 27          2420  406715.767402 28           770  292968.918642 29          3520  145701.079372 30           660  343594.978075 31          3630  405034.547846 32          2310  412579.388504 33          2200  361173.288199 34          1870  401070.997685',
     'sql_generated': '```sql\nSELECT Store_Number, SUM(Total_Sale_Value) AS Total_Sales\nFROM sales\nGROUP BY Store_Number;\n```'},
    {'question': 'What percentage of items were sold on promotion?',
     'sql_result': '   Promotion_Percentage 0              0.625596',
     'sql_generated': "```sql\nSELECT \n    (SUM(CASE WHEN On_Promo = 'Yes' THEN 1 ELSE 0 END) * 100.0) / COUNT(*) AS Promotion_Percentage\nFROM \n    sales;\n```"},
    {'question': 'What was the average transaction value?',
     'sql_result': '   Average_Transaction_Value 0                  19.018132',
     'sql_generated': '```sql\nSELECT AVG(Total_Sale_Value) AS Average_Transaction_Value\nFROM sales;\n```'},
    {'question': 'Create a line chart showing sales in 2021',
     'sql_result': '  sale_month  total_quantity_sold  total_sales_value 0 2021-11-01              43056.0      499984.428193 1 2021-12-01              75724.0      910982.118423',
     'sql_generated': '```sql\nSELECT MONTH(Sold_Date) AS Month, SUM(Total_Sale_Value) AS Total_Sales\nFROM sales\nWHERE YEAR(Sold_Date) = 2021\nGROUP BY MONTH(Sold_Date)\nORDER BY MONTH(Sold_Date);\n```'}
]


class StructureEvaluatedExperiment:
    def __init__(self, answer_questions: List[dict]):
        self.questions: List[dict] = answer_questions
        self.px_client = None
        self.eval_model = None
        self.function_calling_eval = None
        self.evaluate_sql_result = None
        self.evaluate_clarity = None
        self.evaluate_entity_correctness = None
        self.code_is_runnable = None
        self.run_agent_task = None
        self.experiment = None
        self.dataset = None

    def initialize(self):

        self.px_client = px.Client()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        questions_df = pd.DataFrame(self.questions)
        self.dataset = self.px_client.upload_dataset(dataframe = questions_df,
                                      dataset_name=f"overall_experiment_inputs-{now}",
                                      input_keys = ['questions'],
                                      output_keys= ['sql_result', 'sql_generated'])

        self.eval_model = OpenAIModel(model='gpt-4o')

        def function_calling_eval(input, output) -> float:
            if output is None:
                return 0
            function_calls = output.get("tool_calls")
            if function_calls:
                eval_df = pd.DataFrame({
                    "question": [input.get("question")] * len(function_calls),
                    "tool_call": function_calls
                })

                tool_call_eval = llm_classify(
                    data=eval_df,
                    template=TOOL_CALLING_PROMPT_TEMPLATE.template[0].template.replace("{tool_definitions}",
                                                                                       json.dumps(tools_schema).replace("{",
                                                                                                                 '"').replace(
                                                                                           "}", '"')),
                    rails=['correct', 'incorrect'],
                    model=self.eval_model,
                    provide_explanation=True
                )

                tool_call_eval['score'] = tool_call_eval.apply(lambda x: 1 if x['label'] == 'correct' else 0, axis=1)
                return tool_call_eval['score'].mean()
            else:
                return 0

        self.function_calling_eval = function_calling_eval

        def evaluate_sql_result(output, expected) -> bool:
            if output is None:
                return False

            sql_result = output.get('tool_responses')

            sql_result = next((r for r in sql_result if r.get('tool_name') == "lookup_sales_data"), None)

            if not sql_result:
                return True

            sql_result = sql_result.get('tool_response', '')

            result_nums = ''.join(filter(str.isdigit, sql_result))
            expected_nums = ''.join(filter(str.isdigit, expected.get('sql_result')))

            return result_nums == expected_nums

        self.evaluate_sql_result = evaluate_sql_result

        def evaluate_clarity(output, input) -> bool:
            if output is None:
                return False
            df = pd.DataFrame({'query': [input.get('question')],
                               'response': [output.get('final_output')]})

            response = llm_classify(
                data = df,
                template=CLARITY_LLM_JUDGE_PROMPT,
                rails = ['clear', 'unclear'],
                model = self.eval_model,
                provide_explanation=True,
            )

            return response['label'] == 'clear'

        self.evaluate_clarity = evaluate_clarity

        def evaluate_entity_correctness(output, input) -> bool:
            if output is None:
                return False

            df = pd.DataFrame({'query': [input.get('question')],
                               'response': [output.get('final_output')]})

            response = llm_classify(
                data =df,
                template = ENTITY_CORRECTNESS_LLM_JUDGE_PROMPT,
                rails = ['correct', 'incorrect'],
                model = self.eval_model,
                provide_explanation = True
            )

            return response['label'] == 'correct'

        self.evaluate_entity_correctness = evaluate_entity_correctness

        def code_is_runnable(output) -> bool:
            """Check if the code is runnable"""

            if output is None:
                return False
            generated_code = output.get('tool_responses')

            if not generated_code:
                return True

            generated_code = next((r for r in generated_code if r.get('tool_name') == 'generative_visualization'), None)

            if not generated_code:
                return True

            # Get the first response
            generated_code = generated_code.get("tool_response", "")
            generated_code = generated_code.strip()
            generated_code = generated_code.replace("```python", "").replace("```", "")

            try:
                exec(generated_code)
                return True
            except Exception as ex:
                return False

        self.code_is_runnable = code_is_runnable

        def run_agent_task(example: Example):
            print('Starting agent with messages: ', example.input.get('question'))
            messages = [{'role': 'user', 'content': example.input.get('question')}]
            ret = ExampleAgent(get_openai_api_key(), 'GPT-4o-mini').run_with_tracing(messages)
            return process_messages(ret)

        self.run_agent_task = run_agent_task

    def __call__(self, experiment_name = 'Overall Experiment', experiment_description = "Evaluating the overall experiment"):
        self.experiment = run_experiment(self.dataset,
                                         self.run_agent_task,
                                         evaluators = [self.function_calling_eval,
                                                       self.evaluate_sql_result,
                                                       self.evaluate_clarity,
                                                       self.evaluate_entity_correctness,
                                                       self.code_is_runnable],
                                         experiment_name=experiment_name,
                                         experiment_description=experiment_description)

        return self.experiment



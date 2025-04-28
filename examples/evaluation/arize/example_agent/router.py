from examples.evaluation.arize.example_agent.tools import tools, tool_implementations
import json
from typing import List


parquet_file_path = 'data/Store_Sales_Price_Elasticity_Promotions_Data.parquet'
def handle_tool_calls(tool_calls, messages: List[dict], client, model_name):

    for tool_call in tool_calls:
        function = tool_implementations[tool_call.function.name]
        function_args = json.loads(tool_call.function.arguments)
        if tool_call.function.name == 'lookup_sales_data':
            function_args['parquet_file'] = parquet_file_path

        function_args = {**function_args, "openai_client": client, "model_name": model_name}
        result = function(**function_args)

        messages.append({'role': 'tool', 'content': result, "tool_call_id": tool_call.id})

    return messages


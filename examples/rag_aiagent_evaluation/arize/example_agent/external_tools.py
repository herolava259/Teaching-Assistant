from typing import List
from prompts import SQL_GENERATION_PROMPT, DATA_ANALYSIS_PROMPT, CHART_CONFIGURATION_PROMPT, CREATE_CHART_PROMPT
import openai
import pandas as pd
import duckdb
from struture_ouputs import VisualizationConfiguration
from setup_tracing import tracer



def generate_sql_query(prompt: str, columns: List[str], table_name: str, openai_client: openai,
                       model_name: str = 'gpt-4o-mini') -> str:

    """Generate SQL query based on a prompt"""

    formatted_prompt = SQL_GENERATION_PROMPT.format(prompt=prompt,
                                                    columns=columns,
                                                    table_name=table_name)

    response = openai_client.chat.completion.create(
        model = model_name,
        messages=[{'role': 'user', 'content': formatted_prompt}]
    )

    return response.choices[0].message.content

@tracer.tool()
def lookup_sales_data(prompt: str,  table_name:str, parquet_file: str,openai_client) -> str:
    """Implementation of sales data lookup from parquet file using SQL"""
    try:

        df = pd.read_parquet(parquet_file)
        duckdb.sql(f'CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df')

        sql_query = generate_sql_query(prompt, df.columns, table_name, openai_client= openai_client)

        sql_query = sql_query.strip()

        sql_query = sql_query.replace("```sql", "").replace("```", "")

        result = duckdb.sql(sql_query).df()

        return result.to_string()
    except Exception as e:
        return f'Error accessing data: {str(e)}'

@tracer.tool()
def analyze_sales_data(prompt: str, data: str, openai_client: openai, model_name: str = 'gpt-4o-mini') -> str:
    """Implementation of AI-powered sales data analysis"""

    formatted_prompt = DATA_ANALYSIS_PROMPT.format(data=data, prompt=prompt)

    response = openai_client.chat.completion.create(
        model = model_name,
        message = [{'role': 'user', 'content': formatted_prompt}],
    )

    analysis = response.choices[0].message.content

    return analysis if analysis else "No analysis could be generated"

@tracer.chain()
def extract_chart_config(data: str, visualization_goal: str, openai_client: openai, model_name: str) -> dict:
    """Generate chart visualization configuration

    Args:
        data: String containing the data to visualize
        visualization_goal: Description of what the visualization should show

    Returns:
        Dictionary containing line chart configuration
    """

    formatted_prompt = CHART_CONFIGURATION_PROMPT.format(data=data,
                                                         visualization_goal = visualization_goal)

    response = openai_client.beta.chat.completions.parse(
        model= model_name,
        messages=[{'role': 'user', 'content': formatted_prompt}],
        response_format=VisualizationConfiguration
    )

    try:
        content = response.choices[0].message.content

        return {
            "chart_type": content.chart_type,
            "x_axis": content.x_axis,
            "y_axis": content.y_axis,
            "title": content.title,
            "data": data
        }
    except Exception:
        return {
            "chart_type": "line",
            "x_axis": "date",
            "y_axis": "value",
            "title": visualization_goal,
            "data": data
        }

@tracer.chain()
def create_chart(config: dict, openai_client: openai, model_name: str) -> str:
    """Create a chart based on the configuration"""

    formatted_prompt = CREATE_CHART_PROMPT.format(config=config)

    response = openai_client.chat.completions.create(
        model=model_name,
        messages = [{"role": "user", "content": formatted_prompt}]
    )

    code = response.choices[0].message.content

    code = code.replace("'''python").replace("```", "")
    code = code.strip()

    return code

@tracer.tool()
def generate_visualization(data: str, visualization_goal: str, client, model_name) -> str:
    """Generate a visualization based on the data and goal"""

    config = extract_chart_config(data, visualization_goal, client, model_name)

    code = create_chart(config, client, model_name)

    return code


tools_schema = [
    {
        "type": "function",
        "function": {
            "name": "lookup_sales_data",
            "description": "Look up data from Store Sales Price Elasticity Promotions dataset",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The unchanged prompt that the user provided."},
                    "table_name": {"type": "string", "description": "The name of table the one lookup"},
                },
                "required": ["prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_sales_data",
            "description": "Analyze sales data to extract insights",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "The lookup_sales_data tool's output."},
                    "prompt": {"type": "string", "description": "The unchanged prompt that the user provided."}
                },
                "required": ["data", "prompt"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "generate_visualization",
            "description": "Generate Python code to create data visualizations",
            "parameters": {
                "type": "object",
                "properties": {
                    "data": {"type": "string", "description": "The lookup_sales_data tool's output."},
                    "visualization_goal": {"type": "string", "description": "The goal of the visualization."}
                },
                "required": ["data", "visualization_goal"]
            }
        }
    }
]

tool_implementations = {
    "lookup_sales_data": lookup_sales_data,
    "analyze_sales_data": analyze_sales_data,
    "generate_visualization": generate_visualization
}
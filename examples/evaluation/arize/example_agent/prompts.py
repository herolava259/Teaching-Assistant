

SQL_GENERATION_PROMPT = '''
Generate an SQL query based on a prompt. Do not reply with anything besides the SQL query.
The prompt is: {prompt}

The available columns are: {columns}
The table name is: {table_name}
'''

DATA_ANALYSIS_PROMPT = '''
Analyze the following data: {data}
Your job is to answer the following question: {prompt}
'''

CHART_CONFIGURATION_PROMPT = '''
Generate a chart configuration based on this data: {data}
The goal is to show: {visualization_goal}
'''

CREATE_CHART_PROMPT = '''
Write python code to create a chart based on the following configuration.
Only return the code, no other text.
config: {config}
'''

SYSTEM_PROMPT = '''
You are a helpful assistant that can answer questions about the Store Sales Price Elasticity Promotions dataset.
'''
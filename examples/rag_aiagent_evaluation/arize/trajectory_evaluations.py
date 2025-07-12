import phoenix as px
from phoenix.evals import OpenAIModel
from phoenix.experiments import run_experiment, evaluate_experiment
from phoenix.experiments.evaluators import create_evaluator
from phoenix.otel import register
from phoenix.experiments.types import Example
import pandas as pd
from datetime import datetime
from example_agent.ExampleAgent import ExampleAgent
from utils import get_openai_api_key
import os
from typing import List


testing_questions = [
    "What was the average quantity sold per transaction?",
    "What is the mean number of items per sale?",
    "Calculate the typical quantity per transaction",
    "What's the mean transaction size in terms of quantity?",
    "On average, how many items were purchased per transaction?",
    "What is the average basket size per sale?",
    "Calculate the mean number of products per purchase",
    "What's the typical number of units per order?",
    "What is the average number of products bought per purchase?",
    "Tell me the mean quantity of items in a typical transaction",
    "How many items does a customer buy on average per transaction?",
    "What's the usual number of units in each sale?",
    "What is the typical amount of products per transaction?",
    "Show the mean number of items customers purchase per visit",
    "What's the average quantity of units per shopping trip?",
    "How many products do customers typically buy in one transaction?",
    "What is the standard basket size in terms of quantity?"
]

def format_message_steps(messages):
    """
    Convert a list of message objects into a readable format that shows the step taken.

    Args:
        messages (list): A list of message objects containing role, content, tool calls, etc.

    Returns:
        str: A readable string showing the step taken
    """

    steps = []

    for message in messages:
        role = message.get('role')
        content = message.get('content', '')
        if role == 'user':
            steps.append(f'User: {content}')
        elif role == 'system':
            steps.append(f'System: Provided context')
        elif role == 'assistant':
            if message.get('tool_calls'):
                tool_calls = message['tool_calls']
                for tool_call in tool_calls:
                    tool_name = tool_call['function']['name']
                    steps.append(f"Assistant: Called tool '{tool_name}'")
            else:
                steps.append(f"Assistant: {message.get('content')}")

        elif role == 'tool':
            steps.append(f"Tool response: {message.get('content')}")

    return '\n'.join(steps)

def run_agent_and_track_path(example: Example) -> dict:
    messages = [{'role': 'user', 'content': example.input.get('question')}]

    ret = ExampleAgent(get_openai_api_key(), 'GPT-4o-mini').run_with_tracing(messages)

    return {'path_length': len(ret), 'messages': format_message_steps(ret)}



def get_optimal_path_length(experiment):
    outputs = experiment.as_dataframe()['output'].to_dict().values()

    optimal_path_length = min(output.get('path_length') for output in outputs if output and output.get('path_length') is not None)
    return optimal_path_length


class TrajectoryExperiment:
    def __init__(self, convergence_questions: List[str]):
        self.questions = convergence_questions
        self.px_client = None
        self.dataset = None
        self.experiment = None
        self.optimal_path_length = None

    def initialize(self):
        def upload_testing_dataset(px_client):
            convergence_df = pd.DataFrame({
                'question': self.questions
            })

            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            dataset = px_client.upload_dataset(dataframe=convergence_df,
                                               dataset_name=f"convergence_questions-{now}",
                                               input_keys=['question'])

            return dataset
        self.px_client = px.Client()
        self.dataset = upload_testing_dataset(self.px_client)

    def run_experiment(self,experiment_name='Convergence Eval',
                                      description='Evaluating the convergence of the agent'):

        self.experiment = run_experiment(run_agent_and_track_path, experiment_name=experiment_name, experiment_description=description)

        self.optimal_path_length = get_optimal_path_length(self.experiment)

def eval_trajectory_experiment():
    evaluator = TrajectoryExperiment(testing_questions)

    evaluator.initialize()
    evaluator.run_experiment()
    @create_evaluator(name="Convergence Eval", kind="CODE")
    def evaluate_path_length(output) -> float:
        if output and output.get("path_length"):
            return evaluator.optimal_path_length / float(output.get("path_length"))
        else:
            return 0

    experiment = evaluate_experiment(evaluator.experiment, evaluators=[evaluate_path_length])



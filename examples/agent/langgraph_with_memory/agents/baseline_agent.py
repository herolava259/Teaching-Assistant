from ..prompts.triage_system_prompts import triage_system_prompt, triage_user_prompt, agent_system_prompt
from ..prompts.email_assistant_prompt import profile, prompt_instructions, email
from langchain.chat_models import init_chat_model
from ..router_tools.email_assistant_routers import Router
from langgraph.prebuilt import create_react_agent
from ..tools.email_agent_tools import write_email, schedule_meeting, check_calendar_availability
from typing import Dict, List, Callable, Any

class BaselineAgent:
    def __init__(self):
        self.llm = init_chat_model("openai:gpt-4o-mini")
        self.llm_router = self.llm.with_structured_output(Router)
        self.system_prompt = triage_system_prompt.format(
            full_name = profile['full_name'],
            name = profile['name'],
            examples = None,
            user_profile_background = profile["user_profile_background"],
            triage_no = prompt_instructions['triage_rules']["ignore"],
            triage_notify=prompt_instructions["triage_rules"]["notify"],
            triage_email=prompt_instructions["triage_rules"]["respond"],
        )

        self.agent_system_prompt = agent_system_prompt.format(
            instructions=prompt_instructions["agent_instructions"],
            **profile
        )

        self.user_prompt = triage_user_prompt.format(
            author = email['from'],
            to = email['to'],
            subject = email["subject"],
            email_thread = email["body"],
        )

        self.tools = [write_email, schedule_meeting, check_calendar_availability]
        self.agent = create_react_agent("openai:gpt-4o",
                                        tools=self.tools, prompt=self.__create_prompt)

    @staticmethod
    def format_user_message(user_msg: str) -> Dict[str, Any]:

        return {
            "messages":[
                {
                    'role': "user",
                    'content': user_msg
                }
            ]
        }

    def __create_prompt(self, state: dict):

        return [
            {
                'role': 'system',
                'content': self.agent_system_prompt
            }
        ] + state['messages']

    def __call_(self, msg: str):
        state_msg = BaselineAgent.format_user_message(msg)
        return self.agent.invoke(state_msg)


from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing import Literal, TypedDict, Annotated
from langgraph.graph import add_messages

class State(TypedDict):
    email_input: dict
    messages: Annotated[list, add_messages]

class OverallEmailAgentBuilder:
    def __init__(self):
        self.llm_router: Any = None
        self.triage_router: Any = None
        self.react_agent: Any = None

    def gen_llm_router(self, **kwargs) -> Any:
        llm = init_chat_model("openai:gpt-4o-mini")
        self.llm_router = llm.with_structured_output(Router)
        return self

    def gen_triage_router(self, **kwargs) -> Any:

        def triage_router(state: State) -> Command[
            Literal["response_agent", "__end__"]
        ]:
            author = state['email_input']['author']
            to = state['email_input']['to']
            subject = state['email_input']['subject']
            email_thread = state['email_input']['email_thread']

            system_prompt = triage_system_prompt.format(
                full_name=profile["full_name"],
                name=profile["name"],
                user_profile_background=profile["user_profile_background"],
                triage_no=prompt_instructions["triage_rules"]["ignore"],
                triage_notify=prompt_instructions["triage_rules"]["notify"],
                triage_email=prompt_instructions["triage_rules"]["respond"],
                examples=None
            )
            user_prompt = triage_user_prompt.format(
                author=author,
                to=to,
                subject=subject,
                email_thread=email_thread
            )
            result = self.llm_router.invoke(
                [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ]
            )
            if result.classification == "respond":
                print("📧 Classification: RESPOND - This email requires a response")
                goto = "response_agent"
                update = {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Respond to the email {state['email_input']}",
                        }
                    ]
                }
            elif result.classification == "ignore":
                print("🚫 Classification: IGNORE - This email can be safely ignored")
                update = None
                goto = END
            elif result.classification == "notify":
                # If real life, this would do something else
                print("🔔 Classification: NOTIFY - This email contains important information")
                update = None
                goto = END
            else:
                raise ValueError(f"Invalid classification: {result.classification}")
            return Command(goto=goto, update=update)
        self.triage_router = triage_router

        return self

    def gen_react_agent(self, **kwargs) -> Any:
        tools = [write_email, schedule_meeting, check_calendar_availability]
        system_prompt = agent_system_prompt.format(
            instructions=prompt_instructions["agent_instructions"],
            **profile
        )

        def create_prompt(state: dict):
            return [
                {
                    'role': 'system',
                    'content': system_prompt
                }
            ] + state['messages']

        self.react_agent = create_react_agent("openai:gpt-4o",
                                        tools=tools, prompt=create_prompt)
        return self


    def build(self) -> Any:

        email_agent = StateGraph(State)
        email_agent = email_agent.add_node(self.triage_router)
        email_agent = email_agent.add_node('response_agent', self.react_agent)
        email_agent = email_agent.add_edge(START, "triage_router")
        email_agent = email_agent.compile()

        return email_agent



def example_for_using_overall_agent():
    builder = OverallEmailAgentBuilder()

    email_agent = builder.gen_llm_router().gen_triage_router().gen_react_agent().build()

    print('------Example 1------')
    email_input = {
        "author": "Marketing Team <marketing@amazingdeals.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "🔥 EXCLUSIVE OFFER: Limited Time Discount on Developer Tools! 🔥",
        "email_thread": """Dear Valued Developer,

    Don't miss out on this INCREDIBLE opportunity! 

    🚀 For a LIMITED TIME ONLY, get 80% OFF on our Premium Developer Suite! 

    ✨ FEATURES:
    - Revolutionary AI-powered code completion
    - Cloud-based development environment
    - 24/7 customer support
    - And much more!

    💰 Regular Price: $999/month
    🎉 YOUR SPECIAL PRICE: Just $199/month!

    🕒 Hurry! This offer expires in:
    24 HOURS ONLY!

    Click here to claim your discount: https://amazingdeals.com/special-offer

    Best regards,
    Marketing Team
    ---
    To unsubscribe, click here
    """,
    }

    print(email_agent.invoke({"email_input": email_input}))

    print('-----Example 2-----')
    email_input = {
        "author": "Alice Smith <alice.smith@company.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Quick question about API documentation",
        "email_thread": """Hi John,

    I was reviewing the API documentation for the new authentication service and noticed a few endpoints seem to be missing from the specs. Could you help clarify if this was intentional or if we should update the docs?

    Specifically, I'm looking at:
    - /auth/refresh
    - /auth/validate

    Thanks!
    Alice""",
    }

    print(email_agent.invoke({"email_input": email_input}))




        
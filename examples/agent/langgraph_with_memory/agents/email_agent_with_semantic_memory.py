from langgraph.graph import add_messages
from typing import TypedDict, Any, Callable, Annotated, Literal

from ..prompts.triage_system_prompts import triage_system_prompt, triage_user_prompt


class State(TypedDict):
    email_input: dict
    messages: Annotated[list, add_messages]

from langgraph.prebuilt import create_react_agent
from ..prompts.memory_prompts import agent_system_prompt_memory
from ..prompts.email_assistant_prompt import prompt_instructions, profile
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class L1MemoryEmailAgentBuilder:
    def __init__(self):
        self.response_agent: Any = None
        self.response_config: dict|None = None
        self.response_agent_call: Callable | None = None
        self.llm_router: Any = None
        self.triage_router: Any = None
        self.store: Any = None
        self.completed_agent: Any = None
        pass

    def build_react_agent(self, model_name: str = "anthropic:claude-3-5-sonnet-latest") -> Any:
        def create_prompt(state)->list:
            return [
                {
                    "role": "system",
                    "content": agent_system_prompt_memory.format(
                        instructions = prompt_instructions["agent_instructions"],
                        **profile
                    )
                }
            ] + state['messages']

        from ..tools.email_agent_tools import write_email, schedule_meeting, check_calendar_availability
        from ..tools.memory_tools import build_manage_memory_tool, build_search_memory_tool, build_in_memory_store_for_graph

        tools: list = [
            write_email,
            schedule_meeting,
            check_calendar_availability,
            build_search_memory_tool(),
            build_search_memory_tool()
        ]

        self.store = build_in_memory_store_for_graph()

        self.response_agent = create_react_agent(model_name,
                                                 tools=tools,
                                                 prompt=create_prompt,
                                                 store=self.store)

        from langchain_core.runnables.config import RunnableConfig
        self.response_config = RunnableConfig(configurable={"langgraph_user_id": "lance"})

        self.response_agent_call = lambda state : self.response_agent.invoke(state, config=self.response_config)
        return self

    def build_triage_router(self, router_model_name: str = "openai:gpt-4o-mini") -> Any:

        from ..router_tools.email_assistant_routers import Router
        from langchain.chat_models import init_chat_model

        self.llm_router = init_chat_model(router_model_name).with_structured_output(Router)

        def triage_router(state: State) -> Command[Literal["response_agent", "__end__"]]:

            author = state["email_input"]["author"]
            to = state["email_input"]["to"]
            subject = state["email_input"]["subject"]
            email_thread = state["email_input"]["email_thread"]


            system_prompt = triage_system_prompt.format(
                fullname = profile["full_name"],
                name=profile["name"],
                user_profile_background=profile["user_profile_background"],
                triage_no=prompt_instructions["triage_rules"]["ignore"],
                triage_notify=prompt_instructions["triage_rules"]["notify"],
                triage_email =prompt_instructions["triage_rules"]["respond"],
                examples=None
            )

            user_prompt = triage_user_prompt.format(
                author=author,
                to=to,
                subject=subject,
                email_thread=email_thread
            )

            result = self.llm_router.invoke([
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ])

            if result.classification == "respond":
                print("📧 Classification: RESPOND - This email requires a response")
                goto = "respond_agent"
                update = {
                    "messages": [
                        {
                            "role": "user",
                            "content": f"Respond to the email {state["email_input"]}",
                        }
                    ]
                }
            elif result.classification == "ignore":
                print("🚫 Classification: IGNORE - This email can be safely ignored")
                update = None
                goto = END
            elif result.classification == "notify":
                print("🔔 Classification: NOTIFY - This email contains important information")
                update = None
                goto = END
            else:
                raise ValueError(f"Invalid classification: {result.classification}")

            return Command(goto=goto, update=update)

        self.triage_router = triage_router

        return self

    def complete(self) -> Any:
        email_agent = StateGraph(State)
        email_agent = email_agent.add_node(self.triage_router)
        email_agent = email_agent.add_node("response_agent", self.response_agent)
        email_agent = email_agent.add_edge(START, "triage_router")
        self.completed_agent = email_agent.compile(store=self.store)

        return self.completed_agent

    def visualize_workflow_of_agent(self):
        from IPython.display import Image, display

        display(Image(self.completed_agent.get_graph(xray=True).draw_mermaid_png()))



def example_for_using_agent():
    builder = L1MemoryEmailAgentBuilder()
    email_agent = builder.build_react_agent().build_triage_router().complete()
    config = builder.response_config

    print("----Example 1----")
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
    print("email_input:\n", email_input)
    response = email_agent.invoke({"email_input": email_input}, config=config)
    for m in response["messages"]:
        m.pretty_print()

    print("----Example 2----")
    email_input = {
    "author": "Alice Smith <alice.smith@company.com>",
    "to": "John Doe <john.doe@company.com>",
    "subject": "Follow up",
    "email_thread": """Hi John,

Any update on my previous ask?""",
}
    print("email_input:\n", email_input)
    response = email_agent.invoke({"email_input": email_input}, config=config)
    for m in response["messages"]:
        m.pretty_print()






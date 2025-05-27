from ..tools.memory_tools import build_in_memory_store_for_graph
from typing import Any, Optional, Self, List, Dict, TypedDict, Annotated, Literal, Callable
from ..prompts.email_assistant_prompt import email, email_template, profile, prompt_instructions
from ..prompts.triage_system_prompts import triage_system_prompt, triage_user_prompt
from ..router_tools.email_assistant_routers import Router
from langchain.chat_models import init_chat_model
from uuid import uuid4


from langgraph.graph import add_messages
class State(TypedDict):
    email_input: dict
    messages: Annotated[list, add_messages]

from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from typing import Literal
class L3MemEmailAgentBuilder:
    def __init__(self):
        self.llm_router: Any = None
        self.physical_store: Any = None
        self.tools: List[Any] | None = None
        self.triage_router: Callable | None = None
        self.response_agent: Any = None
        self.email_agent: Any = None
        self.prompt_optimizer: Any = None

    def build_triage_router(self, **kwargs) -> Self:
        from langchain.chat_models import init_chat_model

        self.llm_router = init_chat_model("openai:gpt-4o-mini").with_structured_output(Router)
        self.physical_store = build_in_memory_store_for_graph()

        def format_few_shot_example(examples):
            strs = ["Here are some previous examples"]
            for eg in examples:
                strs.append(
                    email_template.format(
                        subject = eg.value["email"]["subject"],
                        to_email = eg.value["email"]["to"],
                        from_email = eg.value["email"]["author"],
                        content = eg.value["email"]["email_thread"][:400],
                        result=eg.value["label"],
                    )
                )
            return "\n\n----------------\n\n".join(strs)

        def triage_router(state: State, config, store) -> Command[
            Literal["response_agent", "__end__"]
        ]:
            author = state['email_input']['author']
            to = state['email_input']['to']
            subject = state['email_input']['subject']
            email_thread = state['email_input']['email_thread']

            namespace = (
                "email_assistant",
                config["configurable"]["langgraph_user_id"],
                "examples"
            )

            examples = self.physical_store.search(
                namespace,
                query = str({"email": state["email_input"]})
            )

            examples = format_few_shot_example(examples)

            langgraph_user_id = config["configurable"]["langgraph_user_id"]
            namespace = (langgraph_user_id, )

            result = self.physical_store.get(namespace, "triage_ignore")
            if result is None:
                self.physical_store.put(namespace,
                                        "triage_ignore",
                                        {"prompt": prompt_instructions["triage_rules"]["ignore"]}
                )
                ignore_prompt = prompt_instructions["triage_rules"]["ignore"]
            else:
                ignore_prompt = result.value["prompt"]


            result = self.physical_store.get(namespace, "triage_notify")
            if result is None:
                store.put(
                    namespace,
                    "triage_notify",
                    {"prompt": prompt_instructions["triage_rules"]["notify"]}
                )
                notify_prompt = prompt_instructions["triage_rules"]["notify"]
            else:
                notify_prompt = result.value['prompt']

            result = self.physical_store.get(namespace, "triage_respond")

            if result is None:
                self.physical_store.put(
                    namespace,
                    "triage_respond",
                    {"prompt": prompt_instructions["triage_rules"]["respond"]}
                )
                respond_prompt = prompt_instructions["triage_rules"]["respond"]
            else:
                respond_prompt = result.value['prompt']

            system_prompt = triage_system_prompt.format(
                full_name=profile["full_name"],
                name=profile["name"],
                user_profile_background=profile["user_profile_background"],
                triage_no=ignore_prompt,
                triage_notify=notify_prompt,
                triage_email=respond_prompt,
                examples=examples
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

    def build_react_agent(self, **kwargs) -> Self:

        from ..tools.memory_tools import build_manage_memory_tool, build_search_memory_tool
        from ..tools.email_agent_tools import write_email, schedule_meeting, check_calendar_availability
        manage_memory_tool = build_manage_memory_tool()
        search_memory_tool = build_search_memory_tool()
        self.tools = [
            write_email,
            schedule_meeting,
            check_calendar_availability,
            manage_memory_tool,
            search_memory_tool
        ]

        from ..prompts.memory_prompts import agent_system_prompt_memory
        def create_prompt(state):
            return [
                {
                    "role": "system",
                    "content": agent_system_prompt_memory.format(
                        instructions=prompt_instructions["agent_instructions"],
                        **profile
                    )
                }
            ] + state['messages']

        from langgraph.prebuilt import create_react_agent

        self.response_agent = create_react_agent(
            "openai:gpt-4o",
            tools=self.tools,
            prompt=create_prompt,
            store=self.physical_store
        )
        return self

    def build_prompt_optimizer(self, **kwargs) -> Self:
        from langmem import create_multi_prompt_optimizer
        self.prompt_optimizer = optimizer = create_multi_prompt_optimizer(
        "anthropic:claude-3-5-sonnet-latest",
                kind="prompt_memory",
        )

    def complete(self):
        from langgraph.graph import StateGraph, START
        email_agent = StateGraph(State)
        email_agent = email_agent.add_node(self.triage_router)
        email_agent = email_agent.add_node("response_agent", self.response_agent)
        email_agent = email_agent.add_edge(START, "triage_router")
        email_agent = email_agent.compile(store=self.physical_store)

        self.email_agent = email_agent
        return email_agent

    def visualize_workflow(self):
        from IPython.display import Image, display

        display(Image(self.email_agent.get_graph(xray=True).draw_mermaid_png()))


    def enhance_instructions(self, conversations: dict):
        prompts = [
            {
                "name": "main_agent",
                "prompt": self.physical_store.get(("lance",), "agent_instructions").value['prompt'],
                "update_instructions": "keep the instructions short and to the point",
                "when_to_update": "Update this prompt whenever there is feedback on how the agent should write emails or schedule events"

            },
            {
                "name": "triage-ignore",
                "prompt": self.physical_store.get(("lance",), "triage_ignore").value['prompt'],
                "update_instructions": "keep the instructions short and to the point",
                "when_to_update": "Update this prompt whenever there is feedback on which emails should be ignored"

            },
            {
                "name": "triage-notify",
                "prompt": self.physical_store.get(("lance",), "triage_notify").value['prompt'],
                "update_instructions": "keep the instructions short and to the point",
                "when_to_update": "Update this prompt whenever there is feedback on which emails the user should be notified of"

            },
            {
                "name": "triage-respond",
                "prompt": self.physical_store.get(("lance",), "triage_respond").value['prompt'],
                "update_instructions": "keep the instructions short and to the point",
                "when_to_update": "Update this prompt whenever there is feedback on which emails should be responded to"

            },
        ]

        updated = self.prompt_optimizer.invoke(
            {"trajectories": conversations, "prompts": prompts}
        )

        for i, updated_prompt in enumerate(updated):
            old_prompt = prompts[i]
            if updated_prompt['prompt'] != old_prompt['prompt']:
                name = old_prompt['name']
                print(f"updated {name}")
                if name == "main_agent":
                    self.physical_store.put(
                        ("lance",),
                        "agent_instructions",
                        {"prompt": updated_prompt['prompt']}
                    )
                else:
                    # raise ValueError
                    print(f"Encountered {name}, implement the remaining stores!")



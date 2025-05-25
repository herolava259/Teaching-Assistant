from ..tools.memory_tools import build_in_memory_store_for_graph
from typing import Any, Optional, Self, List, Dict, TypedDict, Annotated, Literal, Callable
from ..prompts.email_assistant_prompt import email, email_template, profile, prompt_instructions
from ..prompts.triage_system_prompts import triage_system_prompt, triage_user_prompt
from ..router_tools.email_assistant_routers import Router
from langchain.chat_models import init_chat_model
from uuid import uuid4

initial_data = {
    "email": {
        "author": "Sarah Chen <sarah.chen@company.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Update: Backend API Changes Deployed to Staging",
        "email_thread": """Hi John,
    
    Just wanted to let you know that I've deployed the new authentication endpoints we discussed to the staging environment. Key changes include:
    
    - Implemented JWT refresh token rotation
    - Added rate limiting for login attempts
    - Updated API documentation with new endpoints
    
    All tests are passing and the changes are ready for review. You can test it out at staging-api.company.com/auth/*
    
    No immediate action needed from your side - just keeping you in the loop since this affects the systems you're working on.
    
    Best regards,
    Sarah
    """,
    },
    "label": "ignore"
}


from langgraph.graph import add_messages
class State(TypedDict):
    email_input: dict
    messages: Annotated[list, add_messages]
from langgraph.graph import END
from langgraph.types import Command

class L2MemEmailAgentBuilder:
    def __init__(self):
        self.store: Any = None
        self.llm_router: Any = None
        self.tools: List[Callable | Any] | None= None
        self.response_agent: Any = None
        self.response_config = {"configurable": {"langgraph_user_id": "lance"}}
        self.email_agent: Any = None
        self.triage_router: Optional[Callable] = None


    def build_store(self, **kwargs) -> Self:

        self.store = build_in_memory_store_for_graph(embedding_model="openai:text-embedding-3-small")
        self.store.put(
            ("email_assistant", "lance", "examples"),
            str(uuid4()),
            initial_data
        )

        second_data = {
            "email": email,
            "label": "respond"
        }
        self.store.put(
            ("email_assistant",
            "lance",
            "examples"),
            str(uuid4()),
            second_data
        )
        return self

    def build_triage_router(self, **kwargs) -> Self:
        init_chat_model("openai:gpt-4o-mini").with_structured_output(Router)

        def format_few_shot_examples(examples: List[Any]) -> str:

            chains: List[str] = ["Here are some previous examples"]
            for eg in examples:
                chains.append(
                    email_template.format(
                        subject=eg.value["email"]['subject'],
                        to_email=eg.value["email"]["to"],
                        from_email=eg.value["email"]["author"],
                        content=eg.value["email"]["email_thread"][:400],
                        result=eg.value["label"],
                    )
                )
            return "\n\n---------\n\n".join(chains)
        def triage_router(state: State, config, store) -> Command[
            Literal["response_agent", "__end__"]
        ]:
            author = state['email_input']['author']
            to = state['email_input']['to']
            subject = state['email_input']['subject']
            email_thread = state['email_input']['email_thread']

            namespace = (
                "email_assistant",
                config['configurable']['langgraph_user_id'],
                "examples"
            )
            examples = store.search(
                namespace,
                query=str({"email": state['email_input']})
            )
            examples = format_few_shot_examples(examples)

            system_prompt = triage_system_prompt.format(
                full_name=profile["full_name"],
                name=profile["name"],
                user_profile_background=profile["user_profile_background"],
                triage_no=prompt_instructions["triage_rules"]["ignore"],
                triage_notify=prompt_instructions["triage_rules"]["notify"],
                triage_email=prompt_instructions["triage_rules"]["respond"],
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
        from ..tools.email_agent_tools import write_email, schedule_meeting, check_calendar_availability
        from ..tools.memory_tools import build_manage_memory_tool, build_search_memory_tool

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
            store=self.store
        )

        return self

    def complete(self):
        from langgraph.graph import StateGraph, START
        email_agent = StateGraph(State)
        email_agent = email_agent.add_node(self.triage_router)
        email_agent = email_agent.add_node("response_agent", self.response_agent)
        email_agent = email_agent.add_edge(START, "triage_router")
        email_agent = email_agent.compile()

        self.email_agent = email_agent
        return email_agent

    def visualize_workflow(self):
        from IPython.display import Image, display

        display(Image(self.email_agent.get_graph(xray=True).draw_mermaid_png()))


def usage_example():
    builder = L2MemEmailAgentBuilder()
    email_agent = builder.build_store().build_react_agent().build_triage_router().complete()
    config = builder.response_config

    print("---Example 1---")
    email_input = {
        "author": "Tom Jones <tome.jones@bar.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Quick question about API documentation",
        "email_thread": """Hi John - want to buy documentation?""",
    }
    response = email_agent.invoke(
        {"email_input": email_input},
        config={"configurable": {"langgraph_user_id": "harrison"}}
    )

    print("----Example 2----")
    data = {
        "email": {
            "author": "Tom Jones <tome.jones@bar.com>",
            "to": "John Doe <john.doe@company.com>",
            "subject": "Quick question about API documentation",
            "email_thread": """Hi John - want to buy documentation?""",
        },
        "label": "ignore"
    }

    builder.store.put(
        ("email_assistant", "harrison", "examples"),
        str(uuid4()),
        data
    )

    email_input = {
        "author": "Tom Jones <tome.jones@bar.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Quick question about API documentation",
        "email_thread": """Hi John - want to buy documentation?""",
    }
    response = email_agent.invoke(
        {"email_input": email_input},
        config={"configurable": {"langgraph_user_id": "harrison"}}
    )
    print(response)

    print("----Example 3----")
    email_input = {
        "author": "Jim Jones <jim.jones@bar.com>",
        "to": "John Doe <john.doe@company.com>",
        "subject": "Quick question about API documentation",
        "email_thread": """Hi John - want to buy documentation?????""",
    }
    response = email_agent.invoke(
        {"email_input": email_input},
        config={"configurable": {"langgraph_user_id": "harrison"}}
    )

    print(response)

    print("----Example 4----")
    response = email_agent.invoke(
        {"email_input": email_input},
        config={"configurable": {"langgraph_user_id": "andrew"}}
    )
    print(response)


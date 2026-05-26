from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI
from os import environ
from .tools import internet_search
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    base_url="https://api.deepseek.com/",
    api_key=environ["DEEPSEEK_API_KEY"],  # type: ignore
    extra_body={"thinking": {"type": "disabled"}},
)

checkpointer = MemorySaver()

agent = create_deep_agent(
    model=llm,
    tools=[internet_search],
    system_prompt="You are a helpful assistant.",
    checkpointer=checkpointer,
)

config: RunnableConfig = {"configurable": {"thread_id": "default-session"}}


async def run_llm(prompt: str):
    return (
        await agent.ainvoke(
            {"messages": [{"role": "user", "content": prompt}]}, config=config
        )
    )["messages"][-1].content

from deepagents import create_deep_agent
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from os import environ

from .tools import get_weather
from .tools import internet_search

load_dotenv()

llm = ChatOpenAI(
    model="deepseek-v4-flash",
    base_url="https://api.deepseek.com/",
    api_key=environ["DEEPSEEK_API_KEY"],  # type: ignore
    extra_body={"thinking": {"type": "disabled"}},
)


agent = create_deep_agent(
    model=llm,
    tools=[get_weather, internet_search],
    system_prompt="你是一个乐于助人的助手。",
)


def run():
    print(
        agent.invoke({"messages": [{"role": "user", "content": "陈奕迅是谁？"}]})[
            "messages"
        ][-1].content
    )

run()

import asyncio

from langchain_core.runnables import RunnableConfig

from agent.my_agent import agent

config: RunnableConfig = {"configurable": {"thread_id": "session-cli"}}


async def main():
    async for chunk in agent.astream(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "使用子代理完成任何一个简单任务，我来测试你。",
                }
            ]
        },
        stream_mode="updates",
        subgraphs=True,
        version="v2",
        config=config,
    ):
        if chunk["type"] == "updates":
            if chunk["ns"]:
                # Subagent event - namespace identifies the source
                print(f"[subagent: {chunk['ns']}]")
            else:
                # Main agent event
                print("[main agent]")
            print(chunk["data"])


if __name__ == "__main__":
    asyncio.run(main())

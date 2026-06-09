from dataclasses import dataclass
from typing import Literal
from langchain_core.runnables import RunnableConfig
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.getters import query_one
from textual.widgets import Header, Input, Markdown, Static
from agent import agent

config: RunnableConfig = {"configurable": {"thread_id": "session-tui"}}


@dataclass
class Message:
    def __init__(
        self,
        role: Literal[
            "user",
            "agent",
            "system",
            "tool_call",
        ],
        content: str,
    ):
        self.role = role
        self.content = content


class MessageBox(Static):
    def __init__(self, message: Message):
        super().__init__()
        self.message: Message = message

    def compose(self):
        yield Markdown(f"***{self.message.role.upper()}***: {self.message.content}")


class MainScreen(App):
    CSS = """
    """

    context: list[Message] = []
    input = query_one(Input)
    container = query_one("#chat_container", VerticalScroll)

    def __init__(self):
        super().__init__()
        self.title: str = "Breona Agent"
        self.sub_title: str = "GoddoNebianU's Super AI Agent"

    def on_mount(self):
        self.input.focus()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(id="chat_container"):
            for message in self.context:
                yield MessageBox(message)
        yield Input(placeholder="Input your prompt")

    async def on_input_submitted(self, event: Input.Submitted):
        prompt = event.value
        event.input.clear()
        if prompt:
            self.context.append(Message("user", prompt))
            self.input.placeholder = "Thinking..."
            self.input.disabled = True
            self.refresh_chat()

            async for chunk in agent.astream(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt,
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
                        continue
                    else:
                        # Main agent event
                        model_data = chunk["data"].get("model")
                        if not model_data:
                            continue

                        for msg in model_data["messages"]:
                            if msg.content:
                                self.context.append(Message("agent", msg.content))
                            for tc in msg.tool_calls:
                                self.context.append(Message("tool_call", tc["name"]))
                self.refresh_chat()
            self.input.placeholder = "Input your prompt"
            self.input.disabled = False
            self.screen.set_focus(self.input)

    def refresh_chat(self):
        self.container.remove_children()
        for message in self.context:
            self.container.mount(MessageBox(message))
        self.container.scroll_end(animate=True)


if __name__ == "__main__":
    MainScreen().run()

from dataclasses import dataclass
from typing import Literal

from textual import work
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.events import Mount
from textual.getters import query_one
from textual.widgets import Footer, Header, Input, Markdown, Static

from agent.my_agent import run_llm


class MessageBox(Static):
    def __init__(self, message: Message):
        super().__init__()
        self.message: Message = message

    def compose(self):
        yield Markdown(f"***{self.message.role.upper()}***: {self.message.content}")


@dataclass
class Message:
    def __init__(self, role: Literal["user", "agent", "system"], content: str):
        self.role = role
        self.content = content


class MainScreen(App):
    CSS = """
    """

    title: str = "Breona Agent"
    sub_title: str = "GoddoNebianU's Super AI Agent"
    context: list[Message] = [Message("agent", "Hello"), Message("user", "你好")]
    input = query_one(Input)
    container = query_one("#chat_container", VerticalScroll)

    def __init__(self):
        super().__init__()

    def on_mount(self):
        self.input.focus()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(id="chat_container"):
            for message in self.context:
                yield MessageBox(message)
        yield Input(placeholder="Input your prompt")

    @work
    async def on_input_submitted(self, event: Input.Submitted):
        prompt = event.value
        event.input.clear()
        if prompt:
            self.context.append(Message("user", prompt))
            self.refresh_chat()
            self.context.append(Message("agent", await run_llm(prompt)))
            self.refresh_chat()

    def refresh_chat(self):
        self.container.remove_children()
        for message in self.context:
            self.container.mount(MessageBox(message))
        self.container.scroll_end(animate=True)


if __name__ == "__main__":
    MainScreen().run()

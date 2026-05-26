from typing import Annotated
from nonebot import get_plugin_config
from nonebot.adapters import Bot
from nonebot.params import EventPlainText
from nonebot.plugin import PluginMetadata
from nonebot import on_message
from nonebot.adapters.onebot.v11 import PrivateMessageEvent

from agent import run_llm
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="agent",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

matcher = on_message()


@matcher.handle()
async def handle(
    bot: Bot,
    event: PrivateMessageEvent,
    plain_text: Annotated[str, EventPlainText()],
):
    await bot.send(event, run_llm(plain_text))

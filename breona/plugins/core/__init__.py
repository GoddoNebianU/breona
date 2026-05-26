from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="agent",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot import on_command

weather = on_command("天气")

from ....orchestrator.orchestrator import run

run()

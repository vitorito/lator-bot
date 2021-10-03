import logging
import typing

from discord.ext import commands

from lator import Lator
from commands.default_language import DefaultLanguage
from commands.errors import Errors
from commands.help import HelpCommand
from tasks.saver import Saver
from .storage import LanguageStorage


def cogs_setup(bot: commands.Bot) -> None:
    storage = LanguageStorage()
    cogs = [
        Lator(bot, storage),
        Saver(bot, storage),
        DefaultLanguage(bot, storage),
        Errors(),
        HelpCommand(),
    ]

    for cog in cogs:
        bot.add_cog(cog)


def log_setup(level: typing.Any) -> None:
    logger = logging.getLogger("discord")
    logger.setLevel(level)

    handler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w"
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    logger.addHandler(handler)

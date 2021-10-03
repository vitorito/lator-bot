import logging

from discord.ext import commands
from decouple import config

from utils.setup import cogs_setup, log_setup


log_setup(logging.INFO)

bot = commands.Bot(
    command_prefix="-t",
    owner_id=config("OWNER_ID"),
    strip_after_prefix=True,
    help_command=None,
)
cogs_setup(bot)

TOKEN = config("TOKEN")
bot.run(TOKEN)

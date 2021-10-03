import asyncio

from discord.ext import tasks
from discord.ext import commands

from utils.storage import LanguageStorage


class Saver(commands.Cog):
    """Manages the coroutine responsible for saving the data."""

    bot: commands.Bot

    def __init__(self, bot: commands.Bot, storage: LanguageStorage) -> None:
        self.bot = bot
        self.lang_storage = storage

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        await self.save_task.start()

    @tasks.loop(hours=5)
    async def save_task(self) -> None:
        self.lang_storage.save()
        await asyncio.sleep(0)

    @commands.command(name="save", hidden=True)
    @commands.is_owner()
    async def save(self, ctx: commands.Context) -> None:
        self.save_task.restart()
        await ctx.message.delete()

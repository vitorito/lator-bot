import discord
from discord.ext import commands
from discord.colour import Colour
from discord.embeds import Embed

from googletrans.constants import LANGUAGES
from decouple import config

from utils.storage import LanguageStorage


class DefaultLanguage(commands.Cog):
    """Manages default language settings."""

    bot: commands.Bot

    def __init__(self, bot: commands.Bot, storage: LanguageStorage) -> None:
        self.bot = bot
        self.lang_storage = storage

    @commands.command(name="default")
    async def set_default_language(
        self, ctx: commands.Context, language: str
    ) -> None:
        lang = self.lang_storage.get_language(language)
        if not lang:
            default_msg = f"Invalid language: `{language}`"

        else:
            self.lang_storage.set_user_language(str(ctx.author.id), lang)
            default_msg = f"Default language set to `{lang.capitalize()}`"

        await ctx.send(f"{ctx.author.mention} {default_msg}", delete_after=90)

    @commands.command()
    async def languages(self, ctx: commands.Context) -> None:
        languages_channel = self.get_languages_channel()
        msg = f"{ctx.author.mention} Take a look at {languages_channel.mention}. 😎"

        await ctx.send(msg, delete_after=90)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def show_languages(self, ctx: commands.Context):
        await ctx.message.delete()

        languages_channel = self.get_languages_channel()
        if ctx.channel != languages_channel:
            return await self.languages(ctx)

        description = (
            "You can use the full language name or its code to "
            "define your default language.\n\n"
        )

        for code, lang in LANGUAGES.items():
            description += f"{code}: {lang}\n"

        embed = Embed(
            title="Languages", description=description, colour=Colour.random()
        )

        await ctx.send(embed=embed)

    def get_languages_channel(self) -> discord.TextChannel:
        languages_channel_id = int(config("LANGUAGES_CHANNEL"))
        return self.bot.get_channel(languages_channel_id)

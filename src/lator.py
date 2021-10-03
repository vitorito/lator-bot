import discord

from discord.ext import commands
from googletrans import Translator
from googletrans.models import Translated

from utils.storage import LanguageStorage


class Lator(commands.Cog):
    """manages the actions directly linked to the translation of messages."""

    bot: commands.Bot
    lang_storage: LanguageStorage
    translator: Translator

    def __init__(self, bot: commands.Bot, storage: LanguageStorage) -> None:
        self.bot = bot
        self.lang_storage = storage
        self.translator = Translator()

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        activity = discord.Game(name=f"| {self.bot.command_prefix} help |")
        await self.bot.change_presence(activity=activity)

        print(f"Conectado como {self.bot.user}")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.bot.user:
            return

        if self.is_valid(message.content):
            await message.add_reaction("🔄")

    @commands.Cog.listener()
    async def on_reaction_add(
        self, reaction: discord.Reaction, user: discord.User
    ) -> None:
        if user == self.bot.user:
            return

        message = reaction.message

        if self.is_valid(message.clean_content) and reaction.emoji == "🔄":
            dest = self.lang_storage.get_user_language(str(user.id))
            translated_msg = self.translate(message.clean_content, dest=dest)
            src = self.lang_storage.get_language(translated_msg.src)

            embed = self.generate_embed(
                text=translated_msg.text,
                author=message.author,
                requester=user.name,
                src=src,
            )
            await message.channel.send(embed=embed, delete_after=90)

    def generate_embed(
        self, text: str, author: discord.Member, requester: str, src: str
    ) -> discord.Embed:
        embed = discord.embeds.Embed(description=text, colour=author.colour)
        embed.set_author(name=author.name, icon_url=author.avatar_url)
        embed.set_footer(
            text=f"From {src.capitalize()}  •  Requested by {requester}"
        )
        return embed

    def translate(self, msg: str, dest: str, src: str = "auto") -> Translated:
        translated_msg = self.translator.translate(msg, dest=dest)
        return translated_msg

    def is_valid(self, msg: str) -> bool:
        """Check if a message is valid for translation. It will be
        considered valid if there is any letter in it and if it doesn't
        start with the bot command prefix."""
        if msg.startswith(self.bot.command_prefix.strip()):
            return False

        for l in msg:
            if l.isalpha():
                return True
        return False

from discord import Colour
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound

commands_help = {
    "default": {
        "fullname": "-t default <language>",
        "description": (
            "Sets the default language for translations. You can use the full "
            "language name or its code. Type [-t languages] to see the list of "
            "available languages."
        ),
    },
    "languages": {
        "fullname": "-t languages",
        "description": "Shows the list of languages ​​available for translations.",
    },
}


class HelpCommand(commands.Cog):
    """Manages help messages."""

    @commands.command()
    async def help(self, ctx: commands.Context, commands: str = None) -> None:
        global commands_help

        if commands and commands not in commands_help:
            raise CommandNotFound

        embed = Embed(
            title="Help!",
            colour=Colour.random(),
        )

        if commands:
            commands = [commands_help[commands]]

        else:
            commands = commands_help.values()

            greetings = "Hi, I'm Lator, the translator. ^^"
            translation_help = (
                "To translate a message, just click on the 🔄. It will be "
                "translated into the language you set as the default. If you have not "
                "defined a default language, messages will be translated to Portuguese."
            )
            github = (
                "You can see my source code on "
                "[GitHub](https://github.com/vitorito/lator-bot). 😏"
            )
            description = f"{greetings}\n\n{github}\n\n{translation_help}"
            embed.description = description

        for cmd in commands:
            embed.add_field(
                name=cmd["fullname"],
                value=cmd["description"],
                inline=False,
            )

        await ctx.channel.send(embed=embed, delete_after=120)

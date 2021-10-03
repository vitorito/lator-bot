import logging

from discord.ext import commands
from discord.ext.commands.errors import (
    CommandNotFound,
    MissingRequiredArgument,
)


class Errors(commands.Cog):
    """Handles runtime errors."""

    @commands.Cog.listener()
    async def on_command_error(
        self, ctx: commands.Context, error: commands.errors
    ):
        mention = ctx.author.mention

        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                (
                    f"{mention} Missing required arguments. Type `-t help [command]` "
                    "to see the required arguments."
                ),
                delete_after=60,
            )

        elif isinstance(error, CommandNotFound):
            await ctx.send(
                (
                    f"{mention} Command not found. Type `-t help` for the list of all "
                    "available commands."
                ),
                delete_after=60,
            )

        else:
            logging.info(error)

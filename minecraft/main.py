from redbot.core import commands, bot as Bot
from discord.ext.commands import Context

class Minecraft(commands.Cog):
    def __init__(self, bot: Bot): # noqa
        self.bot: Bot = bot

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send('Pong!')
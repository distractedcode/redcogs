from redbot.core import commands, bot as Bot
from discord.ext.commands import Context
import subprocess

class Minecraft(commands.Cog):
    def __init__(self, bot: Bot): # noqa
        self.bot: Bot = bot

    @commands.command()
    async def ping(self, ctx: Context):
        subprocess.run(["tmux", "send-keys", "-t", "CM", "\"say", "meow\"", "enter"])
        await ctx.send('Pong!')
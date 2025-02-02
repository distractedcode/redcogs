from redbot.core import commands, bot as Bot
from discord.ext.commands import Context
from os import system

class Minecraft(commands.Cog):
    def __init__(self, bot: Bot): # noqa
        self.bot: Bot = bot

    @commands.command()
    async def sayHello(self, ctx: Context):
        system('tmux send-keys -t CM "say hello from the bot :)" enter')
        await ctx.send('sent :D')
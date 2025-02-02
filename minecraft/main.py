from redbot.core import commands, bot as Bot, app_commands, Config
import discord
from discord.ext.commands import Context
from os import system

def checkIfContains(stringToCheck: str, stringWithUnsafeCharacters):
    for unsafe in stringWithUnsafeCharacters:
        if unsafe in stringToCheck:
            return True
    return False

class Minecraft(commands.Cog):
    def __init__(self, bot: Bot): # noqa
        self.bot: Bot = bot
        self.config = Config.get_conf(self, identifier=1335182891201724426, force_registration=False)
        default_guild = {
            "allowedWhitelist": []
        }
        self.config.register_guild(**default_guild)



    @commands.command()
    @commands.is_owner()
    async def cobblemon_whitelist(self, ctx: Context, user):
        if len(user) != 16:
            await ctx.send('Username is too long. Contact code if this actually your user LOL')
            return
        if checkIfContains(user, "()-&@*$|%~<>:\"'/\\?!#^*"):
            await ctx.send('Username contains invalid characters.')
            return
        system('tmux send-keys -t CM \"whitelist add' + user + '\" enter')
        await ctx.send('You *should* be whitelisted now.')

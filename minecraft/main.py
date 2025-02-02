from redbot.core import commands, bot as Bot, app_commands, Config
import discord
from discord.ext.commands import Context, check
from os import system
from mcstatus import JavaServer

def checkIfContains(stringToCheck: str, stringWithUnsafeCharacters):
    for unsafe in stringWithUnsafeCharacters:
        if unsafe in stringToCheck:
            return True
    return False

def has_any_role(roles: list):
    async def predicate(ctx: Context):
        userRoles = ctx.author.roles

        for role in roles:
            if ctx.guild.get_role(role) in userRoles: return True
        return False
    return check(predicate)


class Minecraft(commands.Cog):
    def __init__(self, bot: Bot): # noqa
        self.bot: Bot = bot
        self.config = Config.get_conf(self, identifier=1335182891201724426, force_registration=False)
        default_guild = {
            "allowedWhitelist": []
        }
        self.config.register_guild(**default_guild)

    @commands.group()
    async def cobblemon(self, ctx):
        pass

    @cobblemon.command()
    async def list(self, ctx):
        server = JavaServer('localhost', 25565, 5)

        status = server.status()

        players_online = status.players.online
        players_max = status.players.max
        player_list = [player.name for player in status.players.sample] if status.players.sample else "No players online"

        embed = discord.Embed(title=f"Cobblemon :D", color=discord.Color.from_rgb(150, 0, 255))  # Use discord.Color
        embed.add_field(name=f"Players: {players_online}/{players_max}", value=f"", inline=True)
        if isinstance(player_list, list):
            embed.add_field(name="Player List", value=", ".join(player_list), inline=False)
        else:
             embed.add_field(name="Player List", value=player_list, inline=False)
        await ctx.send(embed=embed) # Send the embed

    @cobblemon.group()
    @has_any_role([1155382764984619019, 1335725605072801922]) # Bot Owner's Role, cm_whitelist
    async def whitelist(self, ctx):
        pass

    @whitelist.command(name="add")
    @has_any_role([1155382764984619019, 1335725605072801922]) # Bot Owner's Role, cm_whitelist
    async def whitelist_add(self, ctx: Context, user):
        if len(user) > 16:
            await ctx.send('Username is too long D:')
            return
        if checkIfContains(user, "()-&@*$|%~<>:\"'/\\?!#^*"):
            await ctx.send('Username contains invalid characters.')
            return
        system('tmux send-keys -t CM \"whitelist add ' + user + '\" enter')
        await ctx.send(f'{user} *should* be now whitelisted.')

    @whitelist.command(name="remove")
    @has_any_role([1155382764984619019, 1335725605072801922]) # Bot Owner's Role, cm_whitelist
    async def whitelist_remove(self, ctx: Context, user):
        if len(user) > 16:
            await ctx.send('Username is too long D:')
            return
        if checkIfContains(user, "()-&@*$|%~<>:\"'/\\?!#^*"):
            await ctx.send('Username contains invalid characters.')
            return
        system('tmux send-keys -t CM \"whitelist remove ' + user + '\" enter')
        await ctx.send(f'{user} *should* have been removed from the whitelist')

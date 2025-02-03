from redbot.core import commands, bot as Bot, app_commands, Config
import discord
from discord.ext.commands import Context, check
from os import system
from mcstatus import JavaServer
from mcrcon import MCRcon
from enum import Enum

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

def sendCommandToMinecraftServer(command: str, password = "", port = 25575):
    with MCRcon("localhost", port=port, password=password) as mcr:
        resp = mcr.command("/" + command)
        return resp


class types:
    class pokemonKind(Enum):
        any = 0
        any_generation = 0
        specific = 0


def crystalGenerator(user, limitedUser, item, pokemon, pokeColor, pokemonKind):
    ## This code looks like UTTER shit.
    ## Seperate strings and build at end? LOL
    custom_name = ""
    if pokemonKind == types.pokemonKind.any:
        custom_name += "custom_name='[\"\",{\"text\":\"Ditto\",\"italic\":false,\"color\":\"" + pokeColor + "\"},{\"text\":\" DNA Strand\",\"italic\":false,\"color\":\"aqua\"}]'"
    elif pokemonKind == types.pokemonKind.any_generation:
        raise ValueError('i dont wanna do this right now :(\nDuring command generation: 154: "elif pokemonKind == 1" (a.k.a Generation Pokemon Shard) raised ValueError.')
        # custom_name += "custom_name='[\"\",{\"text\":\"Ditto\",\"color\":\"" + pokeColor + "\"},{\"text\":\" DNA Strand\",\"color\":\"aqua\"}]"
    elif pokemonKind == types.pokemonKind.specific:
        custom_name += "custom_name='[\"\",{\"text\":\"" + pokemon + "\",\"italic\":false,\"color\":\"" + pokeColor + "\"},{\"text\":\" DNA Crystal\",\"italic\":false,\"color\":\"aqua\"}]'"
    # Onto LORE!!!
    lore = "lore=['[\"\",{\"text\":\""
    if pokemonKind == types.pokemonKind.any:
        lore += "A DNA Strand from a Ditto, allowing the modification of the appearance\",\"color\":\"dark_aqua\"}]','[\"\",{\"text\":\"of a pokemon during the process of DNA recombination.\",\"color\":\"dark_aqua\"}]','[\"\"]',"
    elif pokemonKind == types.pokemonKind.specific:
        lore += "A Crystal containing what looks like DNA from " + pokemon + "."

    newLine = '\'[\"\"]\','
    lore += '\'["",{"text":"Give this item to Professor Dark Oak to use it.","italic":false,"color":"#cccccc"}]\','

    #properties
    if pokemonKind == types.pokemonKind.any:
        lore += '\'["",{"text":"Permits Personal Pokemon DNA Modification:","italic":false,"color":"#eeeeee"}]\','
    elif pokemonKind == types.pokemonKind.specific:
        lore += '\'["",{"text":"Grants a ' + pokemon + ' with the following properties:","italic":false,"color":"#eeeeee"}]\','

    if pokeColor == "dark_green": lore += '\'["",{"text":"No additional properties","italic":false,"color":"dark_green"}]\','
    elif pokeColor == "aqua": lore += '\'["",{"text":"is a Shiny","italic":false,"color":"aqua"}]\','
    elif pokeColor == "light_purple": lore += '\'["",{"text":"is a Legendary","italic":false,"color":"light_purple"}]\','
    elif pokeColor == "green": lore += '\'["",{"text":"is a Mythical","italic":false,"color":"green"}]\','
    elif pokeColor == "dark_red": lore += '\'["",{"text":"is a Legendary","italic":false,"color":"light_purple"}]\',' + newLine +  '\'["",{"text":"is a Shiny","italic":false,"color":"aqua"}]\''
    elif pokeColor == "gold": lore += '\'["",{"text":"is a Mythical","italic":false,"color":"green"}]\',' + newLine + '\'["",{"text":"is a Shiny","italic":false,"color":"aqua"}]\''

    if not limitedUser: lore += newLine + '\'["",{"text":"This item was generated for ' + user + '. Only they can use it.","color":"#cccccc"}]\''
    elif limitedUser == "Example": lore += newLine + '\'["",{"text":"This item was generated as an ","color":"red"},{"text":"EXAMPLE","underlined":true,"color":"red"}, {"text":" item. This item is NOT valid.","color":"red"}]\''
    elif limitedUser == "Anyone": pass
    else: lore += newLine + '\'["",{"text":"This item was generated for ' + limitedUser + '","color":"#cccccc"}]\''
    # finish up lore
    lore += ']'

#     return 'give ' + user + ' ' + item + '[' + custom_name + ',' + lore + ']'
    return f'give {user} {item}[{custom_name},{lore}]'


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
        keys: dict = await self.bot.get_shared_api_tokens("minecraft")
        if not keys.get('password'):
            await ctx.send(
                'Please set your rcon password in the Shared API Keys (!!set api) under service "minecraft" with key "password".')
            return
        password = keys.get('password')
        try:
            port = int(keys.get('port')) or 25575
        except:
            port = 25575

        res = sendCommandToMinecraftServer(f'whitelist add {user}', password, port)
        await ctx.send(res)

    @whitelist.command(name="remove")
    @has_any_role([1155382764984619019, 1335725605072801922]) # Bot Owner's Role, cm_whitelist
    async def whitelist_remove(self, ctx: Context, user):
        if len(user) > 16:
            await ctx.send('Username is too long D:')
            return
        if checkIfContains(user, "()-&@*$|%~<>:\"'/\\?!#^*"):
            await ctx.send('Username contains invalid characters.')
            return
        keys: dict = await self.bot.get_shared_api_tokens("minecraft")
        if not keys.get('password'):
            await ctx.send('Please set your rcon password in the Shared API Keys (!!set api) under service "minecraft" with key "password".')
            return
        password = keys.get('password')
        try:
            port = int(keys.get('port')) or 25575
        except:
            port = 25575

        res = sendCommandToMinecraftServer(f'whitelist remove {user}', password, port)
        await ctx.send(res)

    @cobblemon.command(name="send")
    @commands.is_owner()
    async def send(self, ctx: Context, *, command):
        keys: dict = await self.bot.get_shared_api_tokens("minecraft")
        if not keys.get('password'):
            await ctx.send('Please set your rcon password in the Shared API Keys (!!set api) under service "minecraft" with key "password".')
            return
        password = keys.get('password')
        try:
            port = int(keys.get('port')) or 25575
        except:
            await ctx.send('port is not set properly :O')
            port = 25575

        res = sendCommandToMinecraftServer(command, password, port)
        await ctx.send('Sent command.')
        if len(res) <= 4000:
            await ctx.send('Response is too large to send to discord. Sorry!')
            return
        if res != "":
            await ctx.send(res)
from redbot.core import commands, bot as Bot, app_commands, Config
import discord
from discord.ext.commands import Context, check


class code_stuffs(commands.Cog):
    def __init__(self, bot: Bot): # noqa
        self.bot: Bot = bot


    @app_commands.command()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.user_install()
    @app_commands.describe(title="The title of the ticket", messagebody="The description of the ticket")
    @app_commands.rename(title="Title", messagebody="Body")
    async def createTicket(self, interaction: discord.Interaction, title: str, messagebody: str):
        """
        Create a forum post in a forum channel in a private server
        """
        interaction.response.send_message("working", ephemeral=True)


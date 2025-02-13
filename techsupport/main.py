from redbot.core import commands, bot as Bot, app_commands, Config
import discord
from discord.ext.commands import Context, check
from discord.interactions import InteractionResponse


class code_stuffs(commands.Cog):
    def __init__(self, bot: Bot): # noqa
        self.bot: Bot = bot


    @app_commands.command()
    @app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
    @app_commands.describe(title="The title of the ticket", messagebody="The description of the ticket")
    @app_commands.rename(title="title", messagebody="body")
    @app_commands.user_install()
    async def createticket(self, interaction: discord.Interaction, title: str, messagebody: str):
        """
        Create a forum post in a forum channel in a private server
        """
        await interaction.response.send_message("Pong!")

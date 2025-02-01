from .main import Minecraft

async def setup(bot):
    bot.add_cog(Minecraft(bot))

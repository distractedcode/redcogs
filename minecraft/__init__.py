from .main import Minecraft

async def setup(bot):
    await bot.add_cog(Minecraft(bot))

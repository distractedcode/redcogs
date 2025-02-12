from .main import code_stuffs

async def setup(bot):
    await bot.add_cog(code_stuffs(bot))

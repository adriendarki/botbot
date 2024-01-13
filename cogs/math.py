
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


@commands.command()
async def square(self, ctx, number):
    # fais des carré de nombre
    squared_value = int(number) * int(number)
    await ctx.send(str(number) + " squared is " + str(squared_value))


async def setup(bot):
    await bot.add_cog(Math(bot))


from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    async def delete(self, ctx, amount: int = 1):
        """Delete an amount of messages"""
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=amount)
        await ctx.send(f"suppresion de {amount} messages avec succes.", delete_after=3)


async def setup(bot):
    await bot.add_cog(Clear(bot))

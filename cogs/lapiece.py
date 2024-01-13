import random
import discord
from discord.ext import commands


class Piece(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def coinflip(self, ctx):
        """
         command qui un ramdom nummber limité entre 1 et 1000 en fonction du random number tombe sur l'une des
         deux conditions qui sont "pile" ou "face" puis donne le résultat
        """
        random_number = random.randint(1, 1000)
        if random_number >= 500:
            text = 'pile !'
        else:
            text = 'face !'
        header = 'je lance la piece et on tombe sur...'
        embed = discord.Embed()
        embed.add_field(name=header, value=text, inline=True)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Piece(bot))


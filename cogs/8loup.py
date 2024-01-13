import random
from discord.ext import commands


class Loup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='8loup',
                      description=' le loups voit tout',
                      brief=" loup entend tout",
                      aliases=['eight_ball', 'eightball', '8-ball'],
                      pass_context=True)
    async def eight_ball(self, ctx):
        # command avec choix aléatoire définis à l'avance dans des "réponses possible"
        possible_responses = [
            'loup gris',
            'loup bouffie',
            'loup gentil',
            'loup rebelle',
            'loup dormeur',
            'loup prof',
            'loup communiste',
            'loup heureux',
            'loup pet',
            'loup des mers',
            'loup masqué',
            'loup garou',
            'loup aveugle',
            'loup gourmand',
            'loup poutou'
        ]
        await ctx.send(random.choice(possible_responses) + ", " + ctx.message.author.mention)


async def setup(bot):
    await bot.add_cog(Loup(bot))

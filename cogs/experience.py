import discord
from discord.ext import commands
import random
import json
import os


def load_user_data():
    if os.path.exists("users.json"):
        with open("users.json", "r") as file:
            return json.load(file)
    else:
        return {}


def save_user_data(data):
    with open("users.json", "w") as file:
        json.dump(data, file, indent=4)


class Experience(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.users = load_user_data()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.author.bot:
            return

        user_id = str(message.author.id)
        if user_id not in self.users:
            self.users[user_id] = {'xp': 0, 'level': 1}

        xp_to_add = random.randint(10, 20)
        self.users[user_id]['xp'] += xp_to_add
        xp_required = self.users[user_id]['level'] * 100

        if self.users[user_id]['xp'] >= xp_required:
            self.users[user_id]['level'] += 1
            self.users[user_id]['xp'] -= xp_required
            await message.channel.send(
                f"{message.author.mention}, vous êtes maintenant au niveau {self.users[user_id]['level']}!")

        save_user_data(self.users)

    @commands.command()
    async def show_experience(self, ctx):
        user_id = str(ctx.author.id)
        if user_id not in self.users:
            await ctx.send("Vous n'avez pas encore d'XP ou de niveau.")
        else:
            xp = self.users[user_id]['xp']
            level = self.users[user_id]['level']
            await ctx.send(f"{ctx.author.mention}, vous avez {xp} XP et êtes au niveau {level}.")

    @commands.command()
    async def leaderboard(self, ctx):
        if not self.users:
            await ctx.send("Il n'y a pas encore de données à afficher.")
            return

        sorted_users = sorted(self.users.items(), key=lambda x: (x[1]['level'], x[1]['xp']), reverse=True)

        embed = discord.Embed(title="Classement par niveau", color=discord.Color.blue())

        for i, user in enumerate(sorted_users[:10], start=1):
            try:
                member = await ctx.guild.fetch_member(int(user[0]))
                username = member.display_name
            except discord.NotFound:
                username = f"Utilisateur inconnu (ID: {user[0]})"
            level = user[1]['level']
            xp = user[1]['xp']
            embed.add_field(name=f"{i}. {username}", value=f"Niveau: {level}, XP: {xp}", inline=False)

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Experience(bot))

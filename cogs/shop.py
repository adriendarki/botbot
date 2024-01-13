import datetime
import copy
import json
import os
import random
import discord
from discord.ext import commands


def load_points():
    if os.path.exists("points.json"):
        with open("points.json", "r") as f:
            data = json.load(f)
            for user_id in data:
                data[user_id]['last_used'] = datetime.datetime.strptime(data[user_id]['last_used'],
                                                                        "%Y-%m-%dT%H:%M:%S.%f")
            return data
    else:
        return {}


def save_points(points):
    with open("points.json", "w") as f:
        data = copy.deepcopy(points)
        for user_id in data:
            data[user_id]['last_used'] = data[user_id]['last_used'].strftime("%Y-%m-%dT%H:%M:%S.%f")
        json.dump(data, f, indent=4)


def load_role_data():
    if os.path.exists("role_data.json"):
        with open("role_data.json", "r") as file:
            return {int(role_id): price for role_id, price in json.load(file).items()}
    else:
        return {}


def save_role_data(data):
    with open("role_data.json", "w") as file:
        json.dump({str(role_id): price for role_id, price in data.items()}, file)


class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = load_role_data()
        self.points = load_points()

    @commands.command(name="shop")
    async def show_shop(self, ctx):
        if not self.roles:
            await ctx.send("Aucun rôle n'a de prix défini.")
            return

        embed = discord.Embed(title="Boutique de rôles", color=0x00FF00)

        for role_id, price in self.roles.items():
            role = ctx.guild.get_role(role_id)
            if role:
                embed.add_field(name=role.name, value=f"Prix: {price} points", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="buy")
    async def buy_role(self, ctx, *, role_name):
        user_id = str(ctx.author.id)
        user_points = self.points.get(user_id, 0)

        for role_id, price in self.roles.items():
            role = ctx.guild.get_role(role_id)
            if role is not None and role.name.lower() == role_name.lower():
                if user_points >= price:
                    self.points[user_id] -= price
                    save_points(self.points)
                    await ctx.author.add_roles(role)
                    await ctx.send(f"{ctx.author.mention}, vous avez acheté le rôle {role.name} pour {price} points.")
                else:
                    await ctx.send(f"{ctx.author.mention}, vous n'avez pas assez de points pour acheter ce rôle.")
                return

        await ctx.send(f"{ctx.author.mention}, le rôle '{role_name}' n'a pas été trouvé dans la boutique.")

    @commands.command(name="points")
    async def show_points(self, ctx):
        user_id = str(ctx.author.id)
        points = self.points.get(user_id, 0)
        await ctx.send(f"{ctx.author.mention}, vous avez {points} points.")

    @commands.command(name="givepoints")
    @commands.has_permissions(administrator=True)
    async def give_points(self, ctx, member: discord.Member, points_to_give: int):
        user_id = str(member.id)
        if user_id not in self.points:
            self.points[user_id] = 0
        self.points[user_id] += points_to_give
        save_points(self.points)
        await ctx.send(f"{member.mention} a reçu {points_to_give} points.")

    @commands.command(name="random_points", help="Obtenez un nombre aléatoire de points entre 1 et 100.")
    async def random_points(self, ctx):
        user_id = str(ctx.author.id)
        now = datetime.datetime.utcnow()

        if user_id not in self.points:
            self.points[user_id] = {'points': 0, 'last_used': now - datetime.timedelta(days=1)}

        time_since_last_use = now - self.points[user_id]['last_used']
        if time_since_last_use < datetime.timedelta(days=1):
            time_remaining = datetime.timedelta(days=1) - time_since_last_use
            await ctx.send(f"Vous devez attendre {time_remaining} avant de pouvoir utiliser cette commande à nouveau.")
            return

        points = random.randint(1, 100)
        self.points[user_id]['points'] += points
        self.points[user_id]['last_used'] = now
        save_points(self.points)
        await ctx.send(f"Vous avez obtenu {points} points aléatoires!")

    @commands.command(name="set_role_price", help="Définit le prix d'un rôle.")
    @commands.has_permissions(administrator=True)
    async def set_role_price(self, ctx, role: discord.Role, price: int):
        if price < 0:
            await ctx.send("Le prix doit être supérieur ou égal à 0.")
            return

        role_id = role.id
        self.roles[role_id] = price
        save_role_data(self.roles)
        await ctx.send(f"Le prix du rôle {role.name} a été défini à {price} points.")


async def setup(bot):
    await bot.add_cog(Shop(bot))

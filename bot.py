import asyncio
import os

from discord.ext import commands
import discord
import json

with open("token.json", "r") as conffile:
    config = json.load(conffile)

description = '''An example bot to showcase the discord.ext.cogs extension
module.'''

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='/', description=description, intents=intents, )


@bot.event
async def on_ready():
    # information de lancement du bot + activité en cours
    print('en ligne en tant que')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    activity = discord.Game(name="attaquer des poules")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    moji = await bot.get_channel(533707060743766039).send("bot en ligne")
    await moji.add_reaction('🏃')


async def load_extensions():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    async with bot:
        await load_extensions()
        await bot.start(config["token"])


asyncio.run(main())

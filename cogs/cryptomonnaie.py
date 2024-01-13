import json
import aiohttp
from discord.ext import commands
import requests


class Cryptomonnaie(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_crypto_id(self, name_or_symbol):
        url = f"https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url)
        data = response.json()
        for crypto in data:
            if crypto['name'].lower() == name_or_symbol.lower() or crypto['symbol'].lower() == name_or_symbol.lower():
                return crypto['id']
        return None

    def get_crypto_price_and_symbol(self, crypto):
        url = f"https://api.coingecko.com/api/v3/coins/{crypto}"
        response = requests.get(url)
        data = response.json()
        price = data['market_data']['current_price']['usd']
        symbol = data['symbol'].upper()
        return price, symbol

    @commands.command(name='crypto')
    async def crypto_price(self, ctx, name_or_symbol):
        crypto_id = self.get_crypto_id(name_or_symbol)
        if crypto_id is None:
            await ctx.send("La cryptomonnaie demandée n'a pas été trouvée.")
            return

        try:
            price, symbol = self.get_crypto_price_and_symbol(crypto_id)
            await ctx.send(f"Le prix de {name_or_symbol} ({symbol}) est de {price} USD")
        except KeyError:
            await ctx.send("La cryptomonnaie demandée n'a pas été trouvée.")


async def setup(bot):
    await bot.add_cog(Cryptomonnaie(bot))

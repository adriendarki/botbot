from discord.ext import commands
import random
import httpx

GIPHY_API_KEY = "8HWu5PycYYsGEYCAsJheHfyk2k2Me8Cb"


class GIF(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gif(self, ctx, *, search_term=None):
        if search_term is None:
            await ctx.send("Veuillez fournir un terme de recherche pour le GIF.")
            return

        url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={search_term}&limit=10&offset=0&rating=g&lang=fr"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code != 200:
                await ctx.send("Une erreur s'est produite lors de la récupération du GIF.")
                return

            data = response.json()

        if not data["data"]:
            await ctx.send("Aucun GIF trouvé pour cette recherche.")
            return

        gif_choice = random.choice(data["data"])
        gif_url = gif_choice["images"]["original"]["url"]

        await ctx.send(gif_url)


async def setup(bot):
    await bot.add_cog(GIF(bot))

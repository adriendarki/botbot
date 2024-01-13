import discord
from discord.ext import commands


class DirectMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="send_dm", help="Envoie un message privé à un utilisateur hors du serveur.")
    @commands.has_permissions(administrator=True)
    async def send_dm(self, ctx, user_id: int, *, message: str):
        try:
            user = await self.bot.fetch_user(user_id)
            if user is None:
                await ctx.send("Utilisateur introuvable.")
                return

            dm_channel = user.dm_channel
            if dm_channel is None:
                dm_channel = await user.create_dm()

            await dm_channel.send(message)
            await ctx.send(f"Message envoyé à {user.name}#{user.discriminator}")
        except discord.NotFound:
            await ctx.send("Utilisateur introuvable.")
        except discord.Forbidden:
            await ctx.send("Je n'ai pas la permission d'envoyer un message privé à cet utilisateur.")
        except Exception as e:
            print(e)
            await ctx.send("Erreur lors de l'envoi du message privé.")


async def setup(bot):
    await bot.add_cog(DirectMessage(bot))

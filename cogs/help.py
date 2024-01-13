import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command(name="help")
    async def custom_help(self, ctx, *, command_name=None):
        prefix = ctx.prefix
        if command_name is None:
            # Si aucune commande n'est spécifiée, affichez la liste des commandes
            commands_list = [c.name for c in self.bot.commands if not c.hidden]
            commands_str = ', '.join(commands_list)
            help_embed = discord.Embed(title="Commandes disponibles",
                                       description=f"Utilisez `{prefix}help <nom_commande>` pour obtenir de l'aide sur une commande spécifique.",
                                       color=discord.Color.blue())
            help_embed.add_field(name="Commandes", value=commands_str)
            await ctx.send(embed=help_embed)
        else:
            # Si une commande est spécifiée, affichez l'aide pour cette commande
            command = self.bot.get_command(command_name)
            if command is not None and not command.hidden:
                help_embed = discord.Embed(title=f"{prefix}{command.name}",
                                           description=command.help,
                                           color=discord.Color.blue())
                await ctx.send(embed=help_embed)
            else:
                await ctx.send(f"La commande `{command_name}` n'a pas été trouvée.")


async def setup(bot):
    await bot.add_cog(Help(bot))

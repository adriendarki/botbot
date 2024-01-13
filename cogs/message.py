import asyncio
import json
import random
import sys
import time
import discord
import requests
from discord.ext import commands


class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        print(f"Bien regoinds le serveur {member.name}")
        if channel is not None:
            await channel.send(
                "Bienvenue dans la meute {0.mention} ! Fais un petit tour dans #l-assemblée-des-loups pour avoir un "
                "max d'information sur l'antre des loups !".format(
                    member))
            role = discord.utils.get(member.guild.roles, name='Louveteau')
            if role:
                try:
                    await member.add_roles(role)
                    print(f"Rôle 'Louveteau' attribué à {member.name}")
                except discord.Forbidden:
                    print("Le bot n'a pas les autorisations nécessaires pour attribuer le rôle.")
            else:
                print("Le rôle 'Louveteau' n'a pas été trouvé.")
        else:
            print("Aucun canal système trouvé pour envoyer le message de bienvenue.")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = member.guild.system_channel
        await channel.send(" Au revoir {0.mention}, fais un bon voyage :(".format(member))

    @commands.command()
    async def loup(self, ctx):
        # command de définition du bot
        embed = discord.Embed(
            title='LOUP MJ',
            description="yo les petits loups je suis Loup MJ, recommander  par <@226679530063003658> (le chef de la "
                        "meute si ta pas compris) ",
            color=discord.Colour.dark_blue()
        )
        embed.set_footer(text='Loup MJ')
        await ctx.send(embed=embed)

    @commands.command(name='ping')
    async def ping(self, ctx):
        # command de ping permet de savoir le ping du bot
        pingtime = time.time()
        ping = time.time() - pingtime
        await ctx.send(":ping_pong: temps de réponse de `%.01f seconds`" % ping)

    @commands.command()
    async def bonjour(self, ctx):
        # command qui dit bonjour
        await ctx.send("bonjour gamin ")

    @commands.command()
    async def tank(self, ctx):
        # invoque un tank sur le terrain lessivor monte dedans et tu connais la suite
        image = possible_responses = [
            'https://media.giphy.com/media/2a5IGQ1n1Ap1e/giphy.gif',
            'https://media.giphy.com/media/MV5uHhNW7Mw4o/giphy.gif',
            'https://media.giphy.com/media/VmKs3IMpH96Yo/giphy.gif',
            'https://media.giphy.com/media/L18XLtTNCjuelBQa5R/giphy.gif',
            'https://media.giphy.com/media/b35mh8CT4oLK/giphy.gif'
        ]
        embed = discord.Embed(
            title='LOUP MJ',
            description=' attention <@284671200779698186> déboule en tank est te roule dessus. ',
            color=discord.Colour.dark_blue()
        )
        embed.set_image(url=random.choice(possible_responses))
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def name(self, ctx):
        # command retour le nom de utilisateur avec mention
        await  ctx.send("{} c'est bien ton nom ?".format(ctx.message.author.mention))

    @commands.command(name='reverse')
    async def reverse(self, ctx, *args):
        to_reverse = " ".join(args) if len(args) > 0 else ctx.message.content
        await ctx.message.channel.send(to_reverse[::-1])

    @commands.command(name='dit')
    async def dit(self, ctx, *args):
        await ctx.message.delete()
        to_reverse = " ".join(args) if len(args) > 0 else ctx.message.content
        await ctx.message.channel.send(to_reverse)

    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member = None):
        """Simple command which shows the members Top Role."""
        if member is None:
            member = ctx.author
        await ctx.send(f'Le rôle avec le plus de privilèges tenus par {member.display_name} est {member.top_role.name}'
                       f'!')

    @commands.command()
    async def fight(self, ctx, challenger1="", challenger2=""):
        await ctx.send("Ready... FIGHT!!!")
        if challenger1 == "":
            challenger2 = ctx.author.mention
        if challenger2 == "":
            challenger2 = ctx.author.mention
        possible_responses = [
            f'{challenger1} a gagner !',
            f'{challenger2} a gagner !'
        ]
        winner = random.choice(possible_responses)
        await ctx.send(winner)

    @commands.command()
    async def kill(self, ctx, *, target=""):
        await ctx.send("R.I.P " + str(target))
        if target == "":
            target = ctx.message.author.display_name
        await ctx.send(f'{target} est mort!')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def shutdown(self, ctx):
        await ctx.send('**:ok:** bonne nuit  !')
        await self.bot.logout()
        sys.exit(0)

    @commands.command(aliases=['joinme', 'botinvite'])
    async def invite(self, ctx):
        """ Invite le bot sur un serveur  """
        await ctx.send(
            f"**{ctx.author.name}**, utilise ce lien pour m'invitée \n<{discord.utils.oauth_url(self.bot.user.id)}>")

    @commands.command()
    async def source(self, ctx):
        await ctx.send(
            f"**{ctx.bot.user}** tu peux retrouver le code source du bot ici "
            f":\nhttps://github.com/adriendarki/bot-public-lameute")

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx):
        """Affiche des informations sur le serveur"""
        server = ctx.guild
        embed = discord.Embed(title=f"Information sur le serveur {server.name}", color=0x00ff00)
        embed.set_thumbnail(url=server.icon)
        embed.add_field(name="ID", value=server.id, inline=False)
        embed.add_field(name="Owner", value=server.owner, inline=False)
        embed.add_field(name="Membres", value=server.member_count, inline=False)
        embed.add_field(name="Salons", value=len(server.channels), inline=False)
        embed.add_field(name="Rôles", value=len(server.roles), inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="userinfo")
    async def userinfo(self, ctx, *, mention: commands.MemberConverter = None):
        """Affiche des informations sur un utilisateur"""
        user = mention or ctx.author
        roles = [role.name for role in user.roles[1:]]
        if len(roles) == 0:
            roles = ["Aucun rôle"]
        embed = discord.Embed(title=f"Information sur {user}", color=user.color)
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.add_field(name="Nom d'utilisateur", value=user.name, inline=True)
        embed.add_field(name="Tag", value=f"#{user.discriminator}", inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Avatar", value=f"[Lien]({user.display_avatar.url})", inline=True)
        embed.add_field(name="Compte créé le", value=user.created_at.strftime("%d %b %Y à %H:%M"), inline=True)
        embed.add_field(name="Rejoint le serveur le", value=user.joined_at.strftime("%d %b %Y à %H:%M"), inline=True)
        embed.add_field(name="Rôles", value=", ".join(roles), inline=False)
        embed.set_footer(text=f"Demandé par {ctx.author}", icon_url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *, mention: discord.Member = None):
        """Affiche l'avatar d'un utilisateur"""
        user = mention or ctx.author
        embed = discord.Embed(title=f"Avatar de {user.name} ", color=0x00ff00)
        embed.set_image(url=user.display_avatar.url)
        await ctx.send(embed=embed)

    @commands.command()
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        hearts = ['❤', '💛', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        await ctx.send(f"**{ctx.author.name}** has paid their respect {reason}{random.choice(hearts)}")

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def urban(self, ctx, *, search: commands.clean_content):
        """ Find the 'best' definition to your words """
        async with ctx.typing():
            try:
                url = requests.get(f'https://api.urbandictionary.com/v0/define?term={search}', "json").json()
            except Exception:
                return await ctx.send("Urban API returned invalid data... might be down atm.")

            if not url:
                return await ctx.send("I think the API broke...")

            if not len(url['list']):
                return await ctx.send("Couldn't find your search in the dictionary...")

            result = sorted(url['list'], reverse=True, key=lambda g: int(g["thumbs_up"]))[0]

            definition = result['definition']
            if len(definition) >= 1000:
                definition = definition[:1000]
                definition = definition.rsplit(' ', 1)[0]
                definition += '...'

            await ctx.send(f"📚 définition de :  **{result['word']}**```fix\n{definition}```")



    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        """ Give someone a beer! 🍻 """
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.name}**: paaaarty!🎉🍺")
        if user.id == self.bot.user.id:
            return await ctx.send("*drinks beer with you* 🍻")
        if user.bot:
            return await ctx.send(
                f"I would love to give beer to the bot **{ctx.author.name}**, but I don't think it will respond to you :/")

        beer_offer = f"**{user.name}**, you got a 🍺 offer from **{ctx.author.name}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=30.0, check=reaction_check)
            await msg.edit(content=f"**{user.name}** and **{ctx.author.name}** are enjoying a lovely beer together 🍻")
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well, doesn't seem like **{user.name}** wanted a beer with you **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            # Yeah so, bot doesn't have reaction permission, drop the "offer" word
            beer_offer = f"**{user.name}**, you got a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(aliases=['howhot', 'hot'])
    async def hotcalc(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        emoji = "💔"
        if hot > 25:
            emoji = "❤"
        if hot > 50:
            emoji = "💖"
        if hot > 75:
            emoji = "💞"
        if hot > 90:
            emoji = "💞 are you god ?"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command(aliases=['slots', 'bet'])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

    @commands.command()
    async def reactrole(self, ctx, emoji, role: discord.Role, *, message):
        emb = discord.Embed(description=message)
        msg = await ctx.channel.send(embed=emb)
        await msg.add_reaction(emoji)
        with open(r"C:\Users\adrie\PycharmProjects\untitled5\reactrole.json") as json_file:
            data = json.load(json_file)
            new_react_role = {
                'role_name': role.name,
                'role_id': role.id,
                'emoji': emoji,
                'message_id': msg.id
            }
            data.append(new_react_role)
        with open(r"C:\Users\adrie\PycharmProjects\untitled5\reactrole.json", "w") as j:
            json.dump(data, j, indent=4)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        if payload.member.bot:
            pass

        else:
            with open('reactrole.json') as react_file:
                data = json.load(react_file)
                for x in data:
                    if x['emoji'] == payload.emoji.name:
                        role = discord.utils.get(self.bot.get_guild(
                            payload.guild_id).roles, id=x['role_id'])

                        await payload.member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):

        with open('reactrole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name:
                    role = discord.utils.get(self.bot.get_guild(
                        payload.guild_id).roles, id=x['role_id'])

                    await self.bot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

    @commands.command()
    async def serveurco(self, ctx):
        guilds = [guild.name for guild in self.bot.guilds]
        await ctx.send(f"Bot connecté à {len(guilds)} serveurs: {', '.join(guilds)}")


async def setup(bot):
    await bot.add_cog(Message(bot))

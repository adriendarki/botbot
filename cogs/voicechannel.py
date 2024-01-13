import discord
from discord.ext import commands


class TempVoiceChannelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_voice_channels = set()

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        # ID du salon vocal existant pour créer un salon temporaire
        CREATE_TEMP_CHANNEL_ID = 1086753571212628099
        TEMP_CHANNELS_CATEGORY_ID = 1086751635931398204

        if after.channel and after.channel.id == CREATE_TEMP_CHANNEL_ID:
            category = self.bot.get_channel(TEMP_CHANNELS_CATEGORY_ID)
            temp_channel = await category.create_voice_channel(f"{member.name}'s channel")
            self.temp_voice_channels.add(temp_channel.id)
            await member.move_to(temp_channel)
        if before.channel and before.channel.id in self.temp_voice_channels and len(before.channel.members) == 0:
            await before.channel.delete()
            self.temp_voice_channels.remove(before.channel.id)


async def setup(bot):
    await bot.add_cog(TempVoiceChannelCog(bot))

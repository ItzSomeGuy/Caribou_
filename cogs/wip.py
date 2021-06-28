import asyncio
import discord
from discord.ext import commands
import bot


class WIP(commands.Cog):

    def __init__(self, client):
        self.client = client

    # commands
    @commands.command()
    async def mute(self, ctx):
        await ctx.message.delete()

        target = ctx.message.mentions[0]

        await target.edit(mute=True)

    @commands.command()
    async def unmute(self, ctx):
        await ctx.message.delete()

        target = ctx.message.mentions[0]

        await target.edit(mute=False)

    @commands.command(aliases=["csm"])
    async def check_server_member(self, ctx):
        await ctx.message.delete()
        print("server members:")
        for m in bot.server_members:
            print(f"{m}")

    @commands.command(aliases=["fuck zia"])
    async def fuck_zia(self, ctx):
        target = ctx.guild.get_member(728041817882493081)  # zia's ID

        def is_zia(m):
            return m.author == target  # if author is zia

        channels = ctx.guild.text_channels  # get server text channels
        for channel in channels:  # go through channels in server
            await channel.purge(limit=999, check=is_zia)  # if zia delete message


def setup(client):
    client.add_cog(WIP(client))

# async def on_voice_state_update(self, member, before, after):
#         special_channel_id = 735693277059219528
#         guild = member.guild
#         category = guild.get_channel(735693246143004763)
#         br = 128000 if guild.premium_tier > 0 else 96000
#         channel_name = f"{member.name}'s Hole"
#         text_channel_name = f"{member.name}'s Rock"
#
#         if after.channel is not None and after.channel.id == special_channel_id:
#             if member.id == 603269377495924756:
#                 channel_name = "Nic-hole"
#             # if member joins hub channel create private channel
#             new = await guild.create_voice_channel(channel_name,
#                                                    bitrate=br,
#                                                    overwrites=None,
#                                                    category=category,
#                                                    reason=None)
#             perms = new.overwrites_for(member)
#             perms.view_channel = True
#             perms.connect = True
#             perms.move_members = True
#             perms.mute_members = True
#             perms.deafen_members = True
#             await new.set_permissions(member, overwrite=perms)
#
#             print(f"{member.name} dug a hole")
#
#             # move to channel
#             await member.move_to(new)
#
#             # create text channel
#             new = await guild.create_text_channel(text_channel_name)
#
#             perms = new.overwrites_for(member)
#             perms.view_channel = True
#             await new.set_permissions(member, overwrite=perms)
#
#         elif before.channel is not None and before.channel is not after.channel and before.channel.name[
#                                                                                     :-7] == member.name:
#             # if member leaves their private channel, delete the channel
#             print(f"{member.name}'s hole got filled in")
#
#             await before.channel.delete()
#             for c in member.guild.text_channels:
#                 if c.name[-7:] == "'s Rock" and c.category_id == category.id:
#                     await c.delete()
#
#         elif before.channel is not None and before.channel is not after.channel and member.id == 603269377495924756 and before.channel.name == "Nic-hole":
#             # if member leaves their private channel, delete the channel
#             print(f"{member.name}'s hole got filled in'")
#
#             await before.channel.delete()
#
#         # (optional) apply special channel perms
#
#         if after.channel is not None and after.channel.category_id == 735693246143004763:
#             perms = after.channel.overwrites_for(member)
#             perms.view_channel = True
#             perms.connect = True
#             perms.move_members = True
#             await after.channel.set_permissions(member, overwrite=perms)

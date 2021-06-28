import random

import discord
from discord.ext import commands
from discord.utils import get


# use command to make role/channel & announce role [lemme smash]
# this creates a message in the general lfg channel that people can react to and receive the a game-specific lfg role
# people can ping the game-specific lfg channel to get people together to play
# people can take away their reaction to any game-specific lfg announcement to remove the role from themselves
from bot import client


class LFG(commands.Cog):

    def __init__(self, client):
        self.client = client

    # events

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = client.get_guild(193117152709050368)
        user = client.get_user(payload.user_id)
        member = get(client.get_all_members(), id=user.id)
        lfg_channel = guild.get_channel(782766243911827456)
        message = await lfg_channel.fetch_message(payload.message_id)
        role = message.role_mentions[0]

        if member.bot:
            return
        if message.channel.id == lfg_channel.id:
            await member.add_roles(role)

        print(f"added {role.name} to {member.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = client.get_guild(193117152709050368)
        user = client.get_user(payload.user_id)
        member = get(client.get_all_members(), id=user.id)
        lfg_channel = guild.get_channel(782766243911827456)
        message = await lfg_channel.fetch_message(payload.message_id)
        role = message.role_mentions[0]

        if message.channel.id == lfg_channel.id:
            await member.remove_roles(role)

        print(f"removed {role.name} from {member.name}")

    # commands

    # create a game-specific lfg role/channel
    @commands.command(aliases=["lfg"])
    async def create_lfg(self, ctx, game):
        await ctx.message.delete()
        lfg_category = ctx.guild.get_channel(782766156682494002)
        lfg_channel = ctx.guild.get_channel(782766243911827456)

        # create lfg role/channel
        role = await ctx.guild.create_role(name=game, mentionable=True)  # create new role
        channel = await lfg_category.create_text_channel(game)
        await channel.set_permissions(role, read_messages=True)

        # announce lfg role
        message = await lfg_channel.send("a new LFG has been created for " + role.mention + " react with 🤙 to join")
        await message.add_reaction("🤙")

    # delete a game-specific lfg role/channel
    @commands.command()
    async def delete_lfg(self, ctx, game):
        await ctx.message.delete()
        lfg_channel = ctx.guild.get_channel(782766243911827456)
        messages = await lfg_channel.history().flatten()

        # delete lfg role/channel
        await discord.utils.get(ctx.guild.roles, name=game).delete()  # delete game role
        await discord.utils.get(ctx.guild.text_channels, name=game).delete()

        # delete lfg role announcement
        for message in messages:
            if message.role_mentions[0].name == game:
                await message.delete()


def setup(client):
    client.add_cog(LFG(client))

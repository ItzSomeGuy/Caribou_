import asyncio
import random

import discord
from discord.ext import commands
from discord.utils import get


class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    # commands

    # choose one of the provided choices given by the author
    @commands.command()
    async def choose(self, ctx, *args):
        choices = [*args]

        await ctx.channel.send(random.choice(choices))

    # creates a poll (voted for via reactions) that expires after a set time
    @commands.command()
    async def poll(self, ctx):
        pass


def setup(client):
    client.add_cog(Misc(client))

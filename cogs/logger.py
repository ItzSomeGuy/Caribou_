import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord.utils import get


class Logger(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        msg = "(" + str(datetime.datetime.now()).split('.')[0] + ") "
        msg += f"[{message.channel}] "
        msg += message.author.name + ": "

        msg += message.content
        if message.attachments:
            msg += " " + message.attachments[0].url

        log = open(f"cogs/logs/messages/{message.channel}.txt", "a")
        log.write(msg + "\n")
        log.close()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        msg = "(" + str(datetime.datetime.now()).split('.')[0] + ") "
        msg += f"[{message.channel}] "
        msg += "message deleted: "

        msg += message.content
        if message.attachments:
            msg += " " + message.attachments[0].url

        log = open(f"cogs/logs/messages/{message.channel}.txt", "a")
        log.write(msg + "\n")
        log.close()


def setup(client):
    client.add_cog(Logger(client))

# bot.py

import asyncio
import datetime
import random
import os
import csv

import discord
from discord import *
from discord.ext import commands
from discord.ext import tasks
from discord.utils import get

from itertools import cycle

client = commands.Bot(command_prefix="~", intents=discord.Intents.all())
status = cycle(["in the forest", "with the animals", "around"])
client.remove_command("help")
server_members = []
line = ""
TOKEN = None

minute_choice = [2, 5, 10]


@client.event
async def on_ready():
    change_status.start()
    # rename.start()
    print("We have logged in as {0.user}".format(client))

    # members CSV creator

    # member_names = []
    # member_IDs = []
    # insured = []
    # top_roles = []
    # trusted = []
    #
    # members = client.guilds[0].members
    #
    # for m in members:
    #     if not m.bot:
    #         member_names.append(m.name)
    #         member_IDs.append(m.id)
    #         insured.append(False)
    #         top_roles.append(m.top_role)
    #         trusted.append(False)
    #
    # with open('members.csv', mode="w", newline="") as members:
    #     members = csv.writer(members, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
    #
    #     for x in range(len(member_names)):
    #         members.writerow([member_names[x], member_IDs[x], insured[x], top_roles[x], trusted[x]])
    #     print(f"updated members.csv")

    file = "members.csv"

    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        for row in reader:
            server_members.append(row)
    csvfile.close()


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

    server_members.clear()

    file = "members.csv"

    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        for row in reader:
            server_members.append(row)
    csvfile.close()


# @tasks.loop(minutes=random.choice(minute_choice))
# async def rename():
#     members = client.get_guild(193117152709050368).members
#     choices = ["Jeff", "Jimmothy"]
#
#     for member in members:
#         print(f"renamed {member.display_name}")
#         try:
#             await member.edit(nick=random.choice(choices))
#         except:
#             print("error")
#
#         if member.id == 603269377495924756:
#             await member.edit(nick="Nicolseph")


@client.event
async def on_voice_state_update(member, before, after):
    # log mutes/un-mutes

    mute_changed = True if before.mute is not after.mute else False
    self_mute_changed = True if before.self_mute is not after.self_mute else False

    if mute_changed:
        msg = "(" + str(datetime.datetime.now()).split('.')[0] + ") "
        msg += f"{member.name} was server muted" if after.mute else f"{member.name} was server un-muted"

        log = open("log.txt", "a")
        log.write(msg + "\n")
        log.close()
    elif self_mute_changed:
        msg = "(" + str(datetime.datetime.now()).split('.')[0] + ") "
        msg += f"{member.name} muted" if after.self_mute else f"{member.name} un-muted"

        log = open("log.txt", "a")
        log.write(msg + "\n")
        log.close()

# @client.event
# async def on_member_update(before, after):
#     target = 78662784245567488  # target ID
#     n = after.nick
#     if n:
#         last = "JosyJoe"  # desired nickname
#         if after.id == target:
#             await after.edit(nick=last)


# @client.event
# async def on_typing(channel, user, when):
#     scene = channel.guild.get_channel(719280341956689990)
#     victim = channel.guild.get_member(78648083449122816)
#     if channel == scene and user == victim:
#         print(f"silenced {user}")
#         await asyncio.sleep(5)
#         await channel.set_permissions(user, send_messages=False)
#         await asyncio.sleep(10)
#         await channel.set_permissions(user, send_messages=True)


@client.command()
async def update_roles(ctx):
    await ctx.message.delete()

    member_names = []
    top_roles = []

    names_iter = iter(member_names)
    roles_iter = iter(top_roles)

    members = ctx.guild.members
    print(members)

    for m in members:
        if not m.bot:
            member_names.append(m.name)
            top_roles.append(m.top_role)
            print(m.name)
            print(m.top_role)

    temp = []
    file = "members.csv"
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        print(f"{next(roles_iter)}")

        for row in reader:
            current_name = next(names_iter)
            current_role = next(roles_iter)
            if row[3] != current_role:
                row[3] = current_role
            temp.append(row)

        writer = csv.writer(open("members.csv", 'w', newline=""), delimiter=',')

        for row in temp:
            writer.writerow(row)
    csvfile.close()

    print("done!")


@client.command()
async def load(ctx, extension):
    await ctx.message.delete()

    client.load_extension(f"cogs.{extension}")
    print(f"loaded {extension}")


@client.command()
async def unload(ctx, extension):
    await ctx.message.delete()

    client.unload_extension(f"cogs.{extension}")
    print(f"unloaded {extension}")


@client.command()
async def reload(ctx, extension="all"):
    await ctx.message.delete()

    if extension == "all":
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                client.unload_extension(f"cogs.{filename[:-3]}")
                client.load_extension(f"cogs.{filename[:-3]}")
        print(f"reloaded all extensions")
    else:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        print(f"reloaded {extension}")


@client.event
async def on_member_join(member):
    if member.guild.id == 193117152709050368:
        special = False
        specials = []

        for mem in server_members:
            if mem[4] == 'True':
                specials.append(int(mem[1]))

        roles = [get(member.guild.roles, name="DJ"),
                 get(member.guild.roles, name="swingin' hens"),
                 get(member.guild.roles, name="lemme smash"),
                 get(member.guild.roles, name="milk")]
        top_role = None

        for mem in server_members:
            if int(mem[1]) == member.id:
                top_role = get(member.guild.roles, name=mem[3])

        for m in specials:
            if m == member.id:
                special = True

        if special:
            for x in range(3):
                role = roles[x]
                await member.add_roles(role)
                print(f"{member} was given {role}")

            print(f"the new member {member} was special")
        else:
            for x in range(2):
                role = roles[x]
                await member.add_roles(role)
                print(f"{member} was given {role}")

            print(f"the new member {member} was not special")

        if top_role is not None:
            await member.add_roles(top_role)

        await member.add_roles(roles[3])
        await asyncio.sleep(5)
        await member.remove_roles(roles[3])
    elif member.guild.id == 719751252682211362:
        await _insure(member)


@client.event
async def on_member_ban(guild, user):
    special = False
    specials = []

    for mem in server_members:
        if mem[2]:
            specials.append(int(mem[1]))

    for u in specials:
        if u == user.id:
            special = True

    if special:
        user = await client.fetch_user(user.id)
        await guild.unban(user)
        print(f"{user} was pardoned")

        await user.send(f"wow {user.name}! you got beaned lol"
                        f"here ya go, a server invite brought to you by AA Insurance!! https://discord.gg/DPBT78b")
        print(f"invited {user} back")
    else:
        print(f"the member {user} was not special so they gone")

    # send server invite - https://discord.gg/DPBT78b


@client.event
async def on_message(message):
    num = random.randint(1, 100)

    # prevent self-responses
    if message.author == client.user:
        return

    # 100% required 'joe sucks' command
    if message.content.startswith("joe sucks"):
        await message.channel.send("you right, joe does suck")

    # self-insult
    if message.content.startswith("come at me"):
        self_insults = ["You don't smell very good!",
                        "You're like school in July, no class.",
                        "You're as useless as the 'g' in lasagna.",
                        "I don’t think you’re unintelligent. You just have bad luck when it comes to thinking.",
                        "The only way you’ll ever get laid is if you crawl up a chicken’s ass and wait.",
                        "I was pro life before I met you.",
                        "You're the reason the gene pool needs a lifeguard.",
                        "You are more disappointing than an unsalted pretzel.",
                        "You are the human version of period cramps.",
                        "My phone battery lasts longer than your relationships.",
                        "Acting like a prick doesn’t make yours grow bigger."]

        await message.channel.send(random.choice(self_insults))

    # golden egg
    if message.content and num == 36:
        await _golden_egg(message)
        # todo 1st MOTD chance
        # todo one at a time

    await client.process_commands(message)


@client.command()
async def _golden_egg(message):
    if not message.author.bot:
        role = get(message.author.guild.roles, name="golden egg")

        await message.author.add_roles(role)
        await message.add_reaction("🥚")
        print(f"gave {message.author} golden egg!")

        await asyncio.sleep(38600)

        await message.author.remove_roles(role)
        print(f"took away {message.author}'s golden egg!")


@client.command()
async def _insure(member):
    target = member.id
    temp = []
    file = "members.csv"
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        for row in reader:
            if int(row[1]) == target:
                row[2] = True
            temp.append(row)

        writer = csv.writer(open("members.csv", 'w', newline=""), delimiter=',')

        for row in temp:
            writer.writerow(row)
    csvfile.close()

    print(f"insured {member}")


@client.command(aliases=["un-insure"])
async def _uninsure(member):
    target = member.id
    temp = []
    file = "members.csv"
    with open(file, "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        for row in reader:
            if int(row[1]) == target:
                row[2] = False
            temp.append(row)

        writer = csv.writer(open("members.csv", 'w', newline=""), delimiter=',')

        for row in temp:
            writer.writerow(row)
    csvfile.close()

    print(f"un-insured {member}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")

client.run(TOKEN)

# bad bot ideas #

# anti-typing

# music bot

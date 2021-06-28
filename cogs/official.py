import asyncio
import random
import discord
from discord.ext import commands
import bot
from Critter import Critter
from gtts import gTTS
import speech_recognition as sr

critter_list = []


class Official(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        person = member
        critter = None

        guild = member.guild
        spade = 735693277059219528
        br = 128000 if member.guild.premium_tier > 0 else 96000

        possible_holes = []
        for c in critter_list:
            possible_holes.append(c.category_id)

        # set critter
        found = False
        for c in critter_list:
            if c.discord_id == person.id:
                found = True
                critter = c

        if not found:
            critter = Critter(person.id)
            critter_list.append(critter)

        # if user joins Spade channel  ->  create category, voice, text  ->  (give trusted perms)  ->  move user
        if after.channel and after.channel.id == spade:
            # create category
            perms = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False)
            }

            new = await guild.create_category(f"{member.name}", overwrites=perms)
            critter.category_id = new.id

            # create voice channel
            new = await guild.create_voice_channel(f"{member.name}'s Hole",
                                                   bitrate=br,
                                                   category=guild.get_channel(critter.category_id))
            critter.voice_id = new.id

            # set voice perms
            perms = new.overwrites_for(member)

            perms.view_channel = True
            perms.connect = True
            perms.move_members = True
            perms.mute_members = True
            perms.deafen_members = True

            await new.set_permissions(member, overwrite=perms)

            # create text channel
            new = await guild.create_text_channel(f"{member.name}'s Rock",
                                                  category=guild.get_channel(critter.category_id))
            critter.text_id = new.id

            # set text perms
            perms = new.overwrites_for(member)

            perms.view_channel = True
            perms.manage_messages = True

            await new.set_permissions(member, overwrite=perms)

            # move user to hole
            await member.move_to(guild.get_channel(critter.voice_id))

            print(f"{member.name} dug a hole")

        # if user leaves their hole  ->  delete voice, text  ->  delete category
        elif before.channel and after.channel and before.channel.category.id == critter.category_id and after.channel.category.id != critter.category_id:
            channel = guild.get_channel(critter.voice_id)
            await channel.delete()

            channel = guild.get_channel(critter.text_id)
            await channel.delete()

            channel = guild.get_channel(critter.category_id)
            await channel.delete()

            critter_list.remove(critter)

            print(f"{member.name} filled in their hole")

        elif before.channel and before.channel.category.id == critter.category_id and after.channel is None:
            channel = guild.get_channel(critter.voice_id)
            await channel.delete()

            channel = guild.get_channel(critter.text_id)
            await channel.delete()

            channel = guild.get_channel(critter.category_id)
            await channel.delete()

            critter_list.remove(critter)

            print(f"{member.name} filled in their hole")

        # someone hopped in someone's hole
        elif after.channel and after.channel.category.id in possible_holes and before.channel.category.id not in possible_holes:
            hole = None
            for c in critter_list:
                if c.voice_id == after.channel.id:
                    hole = c

            voice = guild.get_channel(hole.voice_id)
            text = guild.get_channel(hole.text_id)

            # set voice perms
            perms = voice.overwrites_for(member)

            perms.view_channel = True
            perms.connect = True
            perms.move_members = True
            perms.mute_members = True
            perms.deafen_members = True

            await voice.set_permissions(member, overwrite=perms)

            # set text perms
            perms = text.overwrites_for(member)

            perms.view_channel = True

            await text.set_permissions(member, overwrite=perms)

            print(f"{member.name} hopped in to {after.channel.name}")

    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]

        other_responses = ["Reply hazy, try again.",
                           "Ask again later.",
                           "Better not tell you now.",
                           "Cannot predict now.",
                           "Concentrate and ask again."]

        if "Aaron" in question or "aaron" in question \
                or "Floy" in question or "floy" in question \
                or "server owner" in question \
                or "SomeGuy" in question or "someguy" in question:

            await ctx.send(f"Question: {question}\nAnswer: {random.choice(other_responses)}")
        else:
            await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

        await ctx.message.delete()

    @commands.command()
    async def ree(self, ctx, *args):
        await ctx.message.delete()

        server = ctx.guild
        channels = server.text_channels
        default = False

        message = " ".join(args[:])

        if message == "":
            message = "@everyone"
            default = True

        for channel in channels:
            msg = await channel.send(message)

            if default:
                await msg.delete()

    @commands.command()
    async def ban(self, ctx):
        await ctx.message.delete()
        target = ctx.message.mentions[0]

        await ctx.guild.ban(target, delete_message_days=0)

    @commands.command()
    async def dunce(self, ctx):
        await ctx.message.delete()
        await ctx.author.edit(nick="poo-poo head", deafen=True)

    @commands.command()
    async def hear(self, ctx):
        await ctx.message.delete()

        if ctx.message.mentions and not ctx.author.id == ctx.message.mentions[0].id:
            target = ctx.message.mentions[0]
            home = target.voice.channel
            people = home.members

            for person in people:
                if not person.id == target.id:
                    await person.edit(mute=True)

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("👋 hello!")

    @commands.command(pass_context=True)
    async def help(self, ctx):
        author = ctx.message.author

        embed = discord.Embed(
            colour=discord.Colour.blurple()
        )

        embed.set_author(name="Help")

        # embed.add_field(name="", value="", inline=False)
        embed.add_field(name="8ball [question]", value="does some spooky shit", inline=False)
        # embed.add_field(name="announce [desired message]", value="sends a message to all channels", inline=False)
        embed.add_field(name="ban [member]", value="beans someone", inline=False)
        embed.add_field(name="choose [choice other_choice another_choice]", value="picks a random choice", inline=False)
        embed.add_field(name="delete_lfg [game]", value="deletes a private role/channel for LFG", inline=False)
        # embed.add_field(name="dunce", value="iunno", inline=False)
        embed.add_field(name="hear [member]", value="helps you hear someone", inline=False)
        embed.add_field(name="unhear [member]", value="for when you don't need to hear someone anymore", inline=False)
        embed.add_field(name="hello", value="used as a greeting or to begin a telephone conversation", inline=False)
        embed.add_field(name="help", value="this..", inline=False)
        embed.add_field(name="insult [member]", value="use it to help win arguments", inline=False)
        embed.add_field(name="join", value="summons the caribou", inline=False)
        embed.add_field(name="leave", value="forces the caribou to retreat", inline=False)
        embed.add_field(name="lfg [game]", value="creates a private role/channel for LFG", inline=False)
        embed.add_field(name="rename [member] [nickname]", value="use to rename a member", inline=False)
        embed.add_field(name="say [words]", value="commands the caribou to speak", inline=False)
        embed.add_field(name="scatter", value="scatters everyone about", inline=False)
        embed.add_field(name="stalk [member]", value="fetches avatar of someone", inline=False)
        # embed.add_field(name="talk [words]", value="makes the bot repeat your words", inline=False)
        embed.add_field(name="throw [member]", value="\"yeetus deletus\" as they say", inline=False)
        embed.add_field(name="pissEveryoneTheFuckOff", value="oof", inline=False)
        # embed.add_field(name="unzip", value="creates a private text channel", inline=False)
        embed.add_field(name="wtf", value="speaks for itself", inline=False)
        # embed.add_field(name="zip", value="closes your private text channel", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def insult(self, ctx):
        target = ctx.message.mentions[0].display_name
        target_insults = [f"{target} doesn't smell very good!",
                          f"{target} is like school in July, no class.",
                          f"{target} is as useless as the 'g' in lasagna",
                          f"{target} sucks more than Donovan's MW KD",
                          f"I don’t think {target} is unintelligent. They just have bad luck when it comes to thinking.",
                          f"The only way {target} will ever get laid is if they crawl up a chicken’s ass and wait.",
                          f"I was pro life before I met {target}.",
                          f"{target} is the reason the gene pool needs a lifeguard.",
                          f"{target} is more disappointing than an unsalted pretzel.",
                          f"{target} is the human version of period cramps.",
                          f"My phone battery lasts longer than {target}'s relationships.",
                          f"Acting like a prick doesn’t make {target}'s grow bigger."]

        await ctx.channel.send(random.choice(target_insults))

    @commands.command()
    async def join(self, ctx):
        await ctx.message.delete()

        channel = ctx.author.voice.channel
        await channel.connect()

    @commands.command()
    async def leave(self, ctx):
        await ctx.message.delete()

        for x in bot.client.voice_clients:
            if x.guild == ctx.message.guild:
                return await x.disconnect()

        return await bot.client.say('fuck you')

    @commands.command()
    async def rename(self, ctx, arg1, *args):
        await ctx.message.delete()

        target = ctx.message.mentions[0]
        new_name = ""

        if args is not None:
            new_name = " ".join(args[:])

        await target.edit(nick=new_name)
        print(f"renamed {target.name} to {new_name}")

    @commands.command()
    async def say(self, ctx, *args):
        await ctx.message.delete()

        author = ctx.author
        target = ctx.guild.get_member(78662784245567488)
        voice_channel = author.voice.channel

        my_text = ' '.join(args)
        print(str(author) + ': ' + my_text)

        language = 'en'
        tld_in = 'ie'

        my_obj = gTTS(text=my_text, lang=language, tld=tld_in, slow=False)
        my_obj.save('test.mp3')

        voice_channel = author.voice.channel

        if voice_channel is not None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio('test.mp3'))
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
            await vc.disconnect()

    @commands.command()
    async def scatter(self, ctx):
        await ctx.message.delete()

        targets = ctx.author.voice.channel.members

        home = ctx.author.voice.channel
        away = None

        channels = ctx.guild.voice_channels

        for target in targets:
            count = random.randint(1, 5)
            away = random.choice(channels)
            print(f"moved {target.display_name} to {away.name} {count} times!")

            for x in range(count):
                await target.move_to(away)
                await target.move_to(home)

    @commands.command()
    async def stalk(self, ctx, target):
        await ctx.message.delete()

        pfp = None
        members = ctx.guild.fetch_members()

        async for m in ctx.guild.fetch_members():
            if m.name == target:
                pfp = m.avatar_url

        if pfp is not None:
            print(pfp)
            await ctx.message.author.send(pfp)

    @commands.command()
    async def talk(self, ctx):
        await ctx.message.delete()

        r = sr.Recognizer()
        mic = sr.Microphone()
        sr.Microphone.list_microphone_names()

        with mic as source:
            audio = r.listen(source)

        # r.recognize_google(audio)

        my_text = r.recognize_google(audio)
        print(my_text)
        language = 'en'

        my_obj = gTTS(text=my_text, lang=language, tld='ie', slow=False)
        my_obj.save('test.mp3')

        voice_channel = ctx.author.voice.channel

        if voice_channel is not None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio('test.mp3'))
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
            await vc.disconnect()

    @commands.command()
    async def throw(self, ctx, arg1, arg2=random.randint(1, 36)):
        await ctx.message.delete()

        target = random.choice(ctx.message.mentions)
        print(f"throwing {target}")

        home = target.voice.channel
        away = None

        count = arg2

        channels = ctx.guild.voice_channels

        away = random.choice(channels)

        await ctx.author.send(f"moved {target.display_name} to {away.name} {count} times!")
        print(f"moved {target.display_name} to {away.name} {count} times!")

        for x in range(count):
            await target.move_to(away)
            await target.move_to(home)

    @commands.command(aliases=["pissEveryoneTheFuckOff", "PETFO"])
    async def torture(self, ctx):
        # TODO add targeting mode

        await ctx.message.delete()

        vc = ctx.message.author.voice.channel
        count = random.randint(1, 36)

        print(f"{count=}")

        for x in range(count):
            target = random.choice(vc.members)
            home = target.voice.channel.id
            punishment = random.randint(0, 2)

            if punishment == 0:
                print(f"muted {target.display_name}")
                await target.edit(mute=True)
                await asyncio.sleep(0.5)
                await target.edit(mute=False)
            elif punishment == 1:
                print(f"deafened {target.display_name}")
                await target.edit(deafen=True)
                await asyncio.sleep(0.5)
                await target.edit(deafen=False)
            elif punishment == 2:
                print(f"threw {target.display_name}")
                await self._throw(target)

            await asyncio.sleep(1)

    @commands.command()
    async def _throw(self, target):
        home = target.voice.channel.id
        away = home
        count = random.randint(1, 5)

        channels = [
            286683678531125248,
            193117152709050369,
            635329541375655946,
            439685524555431936
        ]

        while True:
            temp = random.randint(0, 3)
            if away != temp:
                away = channels[temp]
                break

        h_channel = target.guild.get_channel(home)
        a_channel = target.guild.get_channel(away)

        print(f"moved {target.display_name} {count} times!")

        while count > 0:
            await target.move_to(a_channel)
            await target.move_to(h_channel)

            count = count - 1

    @commands.command()
    async def unhear(self, ctx):
        await ctx.message.delete()

        vc = ctx.message.author.voice.channel
        people = vc.members

        for person in people:
            await person.edit(mute=False)

    @commands.command()
    async def unzip(self, ctx):
        await ctx.message.delete()

        guild = ctx.guild
        member = ctx.author
        critter = None

        # set critter
        found = False
        for c in critter_list:
            if c.discord_id == member.id:
                found = True
                critter = c

        if not found:
            critter = Critter(member.id)
            critter_list.append(critter)

        # create text channel
        perms = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }

        new = await guild.create_text_channel(f"{member.name}'s Pocket",
                                              overwrites=perms)
        critter.set_private_text_id(new.id)

        # set text perms
        perms = new.overwrites_for(member)

        perms.view_channel = True
        perms.manage_messages = True

        await new.set_permissions(member, overwrite=perms)

        print(f"{member.name} opened a pocket")

    @commands.command()
    async def wtf(self, ctx, *args):
        await ctx.message.delete()

        voice_channel = ctx.author.voice.channel

        if voice_channel is not None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            vc.play(discord.FFmpegPCMAudio('wtf.mp3'))
            while vc.is_playing():
                await asyncio.sleep(1)
            vc.stop()
            await vc.disconnect()

    @commands.command()
    async def zip(self, ctx):
        await ctx.message.delete()

        guild = ctx.guild
        member = ctx.author
        channel = None

        for c in critter_list:
            if c.get_discord_id() == member.id:
                channel = guild.get_channel(c.get_private_text_id())

        if channel is not None:
            await channel.delete()

            print(f"{member.name} closed a pocket")


def setup(client):
    client.add_cog(Official(client))

import datetime
import os
import asyncio
import json
import random
import sqlite3

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

load_dotenv()
_token = os.environ['DISCORD_TOKEN']
_intents = discord.Intents.default()
_intents.message_content = True
_intents.members = True
bot = Bot(command_prefix='!', intents=_intents)

with open("help.json", "r") as f:
    help_file = json.load(f)

error = discord.Embed(title="Unknown Error Encountered",
                      color=15548997,
                      timestamp=datetime.datetime.now(),
                      description="There seems to have been an error with the bot.\n"
                                  "Try your command again, and if the problem persists reach out in the Collaboration"
                                  "channel, describing your intended use and exact commands entered."
                      )


def read_cache():
    with open("roles.json", "r") as f:
        roles_cache = json.load(f)
    for role in roles_cache:
        _title = roles_cache[role]['embed']['title']
        _descr = roles_cache[role]["embed"]["description"]
        roles_cache[role]["embed"] = discord.Embed(title=_title,
                                                   description=_descr)
    return roles_cache


def read_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def write_cache(live_cache: dict):
    for role in live_cache.values():
        _title = role['embed'].title
        _descr = role['embed'].description
        role['embed'] = {'title': _title,
                         'description': _descr}
    print(f'live_cache: {live_cache}')
    with open("roles.json", "w") as f:
        json.dump(live_cache, f, indent=2)


@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')
    try:
        db_con = sqlite3.connect("data/bot.sqlite")
        db_cur = db_con.cursor()
        db_cur.execute("CREATE TABLE IF NOT EXISTS user_info(discordID, name, studentID, email)")
        db_con.commit()
        db_con.close()
        print("Database connection successful")
    except Exception as e:
        print(f"Error creating database: {e}")


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    if not message.guild:
        print("DM detected.")

    if "bot is bad" in message.content:
        # send threatening DM
        await message.author.send("I WILL SLAUGHTER YOUR FAMILY!!!!!!!!!!!!")

    #  sadly this does not work yet
    if message.author == "Nelson#8832":
        print("I've been waiting for you, Nelson!!!!")
    if message.author == "nathan#7654":
        print("I've been waiting for you, Nathan!!!!")


@bot.command()
@commands.has_permissions(administrator=True)
async def rm(ctx, arg=None):
    """
    This function posts react-role managers.
    They must be preconfigured and are extracted from "roles.json" on bot startup.
    After the message is sent, the ID of the message is automatically cached and
    associated with the desired role from roles.json.

    Note: Calling this function twice for the same role with overwrite the previously cached ID.
    (for now, only one instance of a role-react may exist at a time).
    Note: When pushing changes to live-server, make sure that the ID's in roles.json match existing ID's

    :param ctx: automatically passed context argument via discordpy.
    :param arg: represents desired keyword for a pre-made role in cache.
    :return: N/a
    """
    await ctx.channel.purge(limit=1)
    if not arg:
        await ctx.send("Incorrect usage... Please pass the title of role from roles.json as argument.")
    else:
        roles_cache = read_cache()
        msg = await ctx.send(embed=roles_cache[arg]["embed"])
        for r in roles_cache[arg]["reacts"].keys():
            await msg.add_reaction(r)
        roles_cache[arg]["ID"] = msg.id
        write_cache(roles_cache)


@bot.event
async def on_raw_reaction_add(payload):
    if payload.member == bot.user:
        return
    roles_cache = read_cache()
    for role in roles_cache:
        if roles_cache[role]["ID"] == payload.message_id:  # enter role making flow
            member = payload.member
            guild = member.guild
            emoji_added = payload.emoji.name
            for emoji in roles_cache[role]['reacts']:
                if emoji_added == emoji:
                    role_desired = discord.utils.get(guild.roles, name=roles_cache[role]['reacts'][emoji])
                    print(roles_cache[role]['reacts'][emoji])
                    print(role_desired)
                    await member.add_roles(role_desired)


@bot.event
async def on_raw_reaction_remove(payload):
    if payload.member == bot.user:
        return
    roles_cache = read_cache()
    for role in roles_cache:
        if roles_cache[role]["ID"] == payload.message_id:  # enter role making flow
            guild = await(bot.fetch_guild(payload.guild_id))
            emoji_added = payload.emoji.name
            for emoji in roles_cache[role]['reacts']:
                if emoji_added == emoji:
                    role_desired = discord.utils.get(guild.roles, name=roles_cache[role]['reacts'][emoji])
                    member = await(guild.fetch_member(payload.user_id))
                    await member.remove_roles(role_desired)


@bot.command()
async def send(ctx, kwarg):
    """
    This function should send messages to desired channels.
    :param ctx: automatically passed context argument via discordpy.
    :param kwarg: name of channel
    :return: N/a
    """
    await ctx.channel.purge(limit=1)
    target_channel = None
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if kwarg in channel.name:
                target_channel = channel
    if target_channel is None:
        _embed = discord.Embed(
            title=f'Error with command($) "send"',
            description=f'Channel {kwarg} was not found in list of channels.\n'
                        f'Please try again and double check the spelling of your channel.\n'
                        f'I am cleaning channel names of emojis, but make sure to match space characters\
                        like "-" and "_".\n'
        )
        await ctx.send(embed=_embed)
        return

    await ctx.send("Channel found, type the message you'd like to send.")

    def check(m):
        return m.channel == ctx.channel and m.author != bot.user

    msg = await bot.wait_for("message", check=check)
    await ctx.channel.purge(limit=2)
    await target_channel.send(msg.content)


@bot.command()
async def feedback(ctx):
    """
    Send anonymous feedback to be reviewed by moderators.

    :param ctx: automatically passed context argument
    :return: N/a
    """
    await ctx.channel.purge(limit=1)
    _embed = discord.Embed(
        title="Confirm Feedback Request",
        description=f'You are about to submit user feedback.\n'
                    f'React with the following for your feedback to be anonymous or public:\n'
                    f'🤐: Anonymous\n'
                    f'🎤: Public'
    )
    msg = await ctx.send(embed=_embed)
    for r in ['🤐', '🎤']:
        await msg.add_reaction(r)

    def check_react(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['🤐', '🎤']

    try:
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check_react)
    except asyncio.TimeoutError:
        await ctx.channel.send('Error: request timeout.')
    else:
        config = read_config()
        await ctx.channel.purge(limit=1)
        if str(reaction.emoji) == '🤐':
            _embed = discord.Embed(title="Submit Feedback",
                                   description="You have 90 seconds to enter your feedback. Your message will be "
                                               "erased and instantly transmitted to a private feedback channel. "
                                               "\nNote: Your entire feedback must be in ONE message (sent at once). If "
                                               "you have a large amount of feedback it is suggested you copy and paste "
                                               "to send it."
                                               "\nThe entire process is 100% anonymous. There are no records kept "
                                               "by the bot nor anyone in control of the bot.")
            await ctx.channel.send(embed=_embed)

            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                msg = await bot.wait_for('message', timeout=90.0, check=check)
            except asyncio.TimeoutError:
                await ctx.channel.send('Error: request timeout.')
                await bot.wait_for('reaction_add', timeout=5.0)
            else:
                channel = bot.get_channel(config["feedback"]["anonymous"])
                await channel.send(embed=discord.Embed(title="Feedback Received",
                                                       timestamp=datetime.datetime.now(),
                                                       description=msg.content))
            await ctx.channel.purge(limit=2)
        elif str(reaction.emoji) == '🎤':
            await ctx.channel.send("You can send public feedback to the dedicated suggestions-feedback channel.\n:)")
            try:
                await bot.wait_for('reaction_add', timeout=5.0)
            except asyncio.TimeoutError:
                await ctx.channel.purge(limit=2)
            else:
                await ctx.channel.send(embed=error)
        else:
            await ctx.channel.send(embed=error)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, q):
    """
    Clear channel of messages.
    Requires administrator permissions.

    :param ctx: automatically passed context argument
    :param q: quantity to clear [n, 'all']
    :return:
    """
    if q == 'all':
        _embed = discord.Embed(
            title=f'Purging {ctx.channel}...\n'
                  f'Confirm with ☠️ or react 🛑 to cancel.'
        )
        msg = await ctx.send(embed=_embed)
        await msg.add_reaction('☠️')
        await msg.add_reaction('🛑')

        def confirm(reaction, user):
            return user == ctx.message.author and (str(reaction.emoji) == '☠️' or str(reaction.emoji) == '🛑')

        try:
            _reaction, _user = await bot.wait_for('reaction_add', timeout=10.0, check=confirm)
        except asyncio.TimeoutError:
            await ctx.channel.purge(limit=2)
            await ctx.send("https://media.giphy.com/media/6q29hxDKvJvPy/giphy.gif")
            await ctx.send("Purge aborted...")
        else:
            if _reaction.emoji == '☠️':
                await ctx.channel.purge()
                await ctx.send("https://imgur.com/r/gifs/rlfYxNj")
                await ctx.send(f'{ctx.channel} has been purged...')
            else:
                await ctx.channel.purge(limit=3)
                await ctx.send("https://media.giphy.com/media/6q29hxDKvJvPy/giphy.gif")
                await ctx.send("Purge aborted...")

    else:
        await ctx.channel.purge(limit=(int(q) + 1))
        await ctx.channel.send(f'{int(q) + 1} messages cleared from {ctx.channel}.')


@bot.command()
async def release(ctx):
    """
    Display most recent release notes.

    :param ctx:
    :return: N/a
    """
    await ctx.channel.purge(limit=1)
    with open("release_notes.md", "r") as f:
        notes = f.read()
    # notes = "```" + notes + "```"
    _embed = discord.Embed(title="Latest Release Notes:",
                           description=notes)
    await ctx.send(embed=_embed)


@bot.command()
async def rps(ctx):
    """
    This function allows you to play Rock-Paper-Scissors with the discord bot.
    :param ctx:
    :return: N/A
    """
    embed = discord.Embed(
        title="Welcome to the Rock-Paper-Scissors game !!!",
        description="Rock, Paper, or Scissors? Choose wisely ... 🥸",
        color=discord.Colour.yellow()
    )
    choices_rps = ["rock🪨", "paper🧻 ", "scissors✂️"]
    choices_reg = ["rock", "paper", "scissors"]
    await ctx.send(embed=embed)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in choices_reg

    user_choice = await bot.wait_for('message', check=check)
    user_choice = user_choice.content

    pc_choice = random.choice(choices_rps)
    print(f'User Choice: \n{user_choice}')
    print(f'PC Choice: \n{pc_choice}')

    #   Let's set the conditions for rock
    if user_choice == 'rock':
        if "rock" in pc_choice:
            await ctx.send(f"Woah!!! we really had to tie 🫥.\n Your choice:")
            await ctx.send(file=discord.File('assets/ro.jpg'))
            await ctx.send("Bots choice:")
            await ctx.send(file=discord.File('assets/ro.jpg'))
        elif "paper" in pc_choice:
            await ctx.send(
                f"I'm smarter that's why I WIN,you can't beat me 😎 \nYour choice:")
            await ctx.send(file=discord.File('assets/ro.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/pap.jpg'))
        elif "scissors" in pc_choice:
            await ctx.send(
                f"HOLY, You must have used all your luck. Congratulations you win 🎉🥳. \nYour choice: ")
            await ctx.send(file=discord.File('assets/ro.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/sci.jpg'))

    #   Let's set the conditions for paper
    if user_choice == 'paper':
        if "paper" in pc_choice:
            await ctx.send(f'Wouh!!! You really wanted to settle for a draw 🫥  .\nYour choice: ')
            await ctx.send(file=discord.File('assets/pap.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/pap.jpg'))
        elif "scissors" in pc_choice:
            await ctx.send(f"Welp, what can I say don't me tell you taught you had a chance 😎 \nYour choice: ")
            await ctx.send(file=discord.File('assets/pap.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/sci.jpg'))
        elif "rock" in pc_choice:
            await ctx.send(
                f"Their must have been a bugged somewhere, but Congratulations you win 🥳🎉  \nYour choice:")
            await ctx.send(file=discord.File('assets/pap.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/ro.jpg'))

    #   Let's set the conditions for scissors
    if user_choice == 'scissors':
        if "scissors" in pc_choice:
            await ctx.send(f"Unfortunately it's a tie 🫥  .\n Your choice: ")
            await ctx.send(file=discord.File('assets/sci.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/sci.jpg'))
        elif "rock" in pc_choice:
            await ctx.send(
                f" Like we didn't already know that i would win 😎 \nYour choice: ")
            await ctx.send(file=discord.File('assets/sci.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/ro.jpg'))
        elif "paper" in pc_choice:
            await ctx.send(
                f"My developer is a newbie so I'll let you have this one 🥳🎉\nYour choice: ")
            await ctx.send(file=discord.File('assets/sci.jpg'))
            await ctx.send("Bot choice:")
            await ctx.send(file=discord.File('assets/pap.jpg'))


# @bot.command()
# async def guess(ctx):
#     embed = discord.Embed(
#         title="Guessing Game 🥸👀",
#         description="Try and guess the number I'm thinking.🤔\nYou only get 3 chances to guess the correct number."
#                     "\nDkn what to put yet!!!",
#
#         color=discord.Colour.red()
#     )
#     tries = 3
#     number = random.randrange(50)                                   STILL  UNDER WORK
#     amount_tries = 0
#     await ctx.send(embed=embed)
#
#     def check(msg):
#         return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()
#
#     user_choice = await bot.wait_for('message', check=check)
#     while tries == 3:
#         user_choice = await bot.wait_for('message', check=check)
#         user_choice = user_choice.content
#         print("hello")
#         if user_choice == number:
#             await ctx.send("Congrats you found the number")


@bot.command()
async def grps(ctx, size, min_size):
    """
    :param ctx: automatically passed context argument
    :param size: defines the maximum size of the group
    :param min_size: defines the minimum size of the group
    :return: Nothing
    """
    import random

    # Define a function to check for valid integer inputs
    def is_valid_int(input_str):
        try:
            input_int = int(input_str)
            return input_int > 0
        except ValueError:
            return False

    # Check that the size and min_size arguments are valid integers
    if not is_valid_int(size) or not is_valid_int(min_size):
        await ctx.send("Please enter valid integer arguments for the minimum and maximum size of the group .")
        return

    # Convert the size and min_size arguments to integers
    size = int(size)
    min_size = int(min_size)

    # Create an embed for the message to react to
    embed = discord.Embed(
        title="Group generator",
        description="React to this message to get assigned to a group. Press 🛑 to stop the program",
        color=discord.Colour.yellow()
    )

    # Send the message and add the reactions
    message = await ctx.send(embed=embed)
    await message.add_reaction('👍')
    await message.add_reaction('🛑')

    # Define a function to check for valid reactions from non-bot users
    def check(reaction, user):
        return user != bot.user and str(reaction.emoji) in ['👍', '🛑'] and reaction.message.id == message.id

    # Wait for reactions for 1 minute
    try:
        while True:
            reaction, user = await bot.wait_for('reaction_add', timeout=60, check=check)

            # If someone presses the stop button, shuffle members into groups
            if str(reaction.emoji) == '🛑':
                random.shuffle(members)
                num_groups = len(members) // size + int(len(members) % size != 0)
                groups = [members[i * size:(i + 1) * size] for i in range(num_groups)]

                # Send a message to each member of each group
                for i, group in enumerate(groups):
                    group_str = ", ".join(member.mention for member in group)
                    for member in group:
                        await member.send(f"{member.mention}. You are in group {i + 1} with: {group_str} ")

                # Send a message to the channel that the groups have been formed
                await ctx.send("Groups have been formed!")
                break

            # If someone presses the join button, add them to the members list
            elif str(reaction.emoji) == '👍':
                members = []
                async for user in reaction.users():
                    if user != bot.user:
                        members.append(user)

                members = [await bot.fetch_user(member.id) for member in members]

    except asyncio.TimeoutError:
        await ctx.send("Group forming has been closed...")
        return

    # Check if there are enough members to form a group
    if len(members) < min_size:
        await ctx.send("Not enough people reacted to form a group.")
        return

    # If there are enough members, but not enough to form a full group, make a group with all of them
    elif len(members) < size:
        group_str = ", ".join(member.mention for member in members)
        for member in members:
            await member.send(f"{member.mention}, you are in")


# will eventually need to replace with database
temp_user_data = {}


@bot.command()
async def verify(ctx):
    """
    Enter the verification process.
    Gathers and stores students' email, name, and student ID.

    :param ctx:
    :return:
    """
    await ctx.author.send("Welcome to the verification process!")
    await ctx.author.send("Please enter your email address.")

    def _check(msg):
        return msg.author == ctx.author and msg.channel == ctx.author.dm_channel

    try:
        email = await bot.wait_for('message', check=_check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond. Please try again.")
        return

    await ctx.author.send("Please enter your full name (first and last).\nSeperated by a space. (ex. John Doe)")
    try:
        name = await bot.wait_for('message', check=_check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond. Please try again.")
        return

    await ctx.author.send("Please enter your student ID.")
    try:
        student_id = await bot.wait_for('message', check=_check, timeout=30)
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond. Please try again.")
        return
    temp_user_data[ctx.author.id] = {
        "email": email.content,
        "name": name.content,
        "student_id": student_id.content
    }
    await ctx.author.send("Here is the information you entered:")
    await ctx.author.send(f"Email: {temp_user_data[ctx.author.id]['email']}")
    await ctx.author.send(f"Name: {temp_user_data[ctx.author.id]['name']}")
    await ctx.author.send(f"Student ID: {temp_user_data[ctx.author.id]['student_id']}")
    confirmation = await ctx.author.send(
        "Is this information correct? Your attendance will depend on it (especially ID).")
    await confirmation.add_reaction("✅")
    await confirmation.add_reaction("❌")

    def confirm_check(reaction, user):
        print("reaction noticed")
        return user == ctx.message.author and str(reaction.emoji) in ["✅", "❌"]

    try:
        _reaction, _user = await bot.wait_for('reaction_add', check=confirm_check, timeout=30)
        print(_reaction, _user)
    except asyncio.TimeoutError:
        await ctx.author.send("You took too long to respond. Please restart verification process.")
        return
    if str(_reaction.emoji) == "❌":
        await ctx.author.send("Please restart the verification process.")
        return
    elif str(_reaction.emoji) == "✅":
        # add to database
        try:
            db_con = sqlite3.connect("data/bot.sqlite")
            db_cur = db_con.cursor()
            db_cur.execute("SELECT * FROM user_info WHERE discordID = ?", (ctx.author.id,))
            if db_cur.fetchone():  # Update
                db_cur.execute("UPDATE user_info SET email = ?, name = ?, studentID = ? WHERE discordID = ?", (
                    temp_user_data[ctx.author.id]['email'],
                    temp_user_data[ctx.author.id]['name'],
                    temp_user_data[ctx.author.id]['student_id'],
                    ctx.author.id
                ))
                db_con.commit()
                db_con.close()
            else:  # New entry
                db_cur.execute("INSERT INTO user_info VALUES (?, ?, ?, ?)", (
                    ctx.author.id,
                    temp_user_data[ctx.author.id]['email'],
                    temp_user_data[ctx.author.id]['name'],
                    temp_user_data[ctx.author.id]['student_id']
                ))
                db_con.commit()
                db_con.close()
        except Exception as e:
            print(e)
            await ctx.author.send("There was an error saving your information to the database. Please try again. If "
                                  "the problem persists, please contact a moderator.")
            return
        await ctx.author.send(
            "Thank you for verifying your information. You will be notified when your information has "
            "been verified.")
        await ctx.author.send("If you need to change your information, please use !verify again.")


@bot.command()
async def me(ctx):
    """
    Get the user's data from the database.

    :param ctx:
    :return:
    """
    await ctx.send(f"Sending data for user {ctx.author.name}...")
    try:
        db_con = sqlite3.connect("data/bot.sqlite")
        db_cur = db_con.cursor()
        db_cur.execute("SELECT * FROM user_info WHERE discordID=?", (ctx.author.id,))
        data = db_cur.fetchone()
        all_data = db_cur.fetchall()
        for row in all_data:
            print(row)
        db_con.close()
        if data is None:
            await ctx.author.send("No data found. Please verify your information using !verify.")
            return
        else:
            await ctx.author.send("Here is your data:")
            await ctx.author.send(f"Email: {data[1]}")
            await ctx.author.send(f"Name: {data[2]}")
            await ctx.author.send(f"Student ID: {data[3]}")
    except KeyError:
        await ctx.author.send("No data found. Please verify your information using !verify.")


@bot.command()
@commands.has_permissions(administrator=True)
async def attendance(ctx, url=None):
    """
    Uses the user's data to submit attendance via Google form.

    :param ctx: automatically passed by discord.py
    :param url: the url of the Google form
    :return:
    """
    emoji = "🤠"
    if url is None:
        await ctx.send("Invalid usage. Please use !attendance <url>")
        return
    await ctx.message.delete()
    attendance_embed = discord.Embed(title=f'Attendance for DATE',
                                     description=f'We must take attendance.')
    attendance_embed.add_field(name="How To",
                               value="If your student info is properly linked to your discord account, "
                                     f"you can simply react to this message with {emoji}, and a filled "
                                     "attendance form will be generated for you.\nIf your discord account"
                                     " is unlinked, you must fill out the google form linked below.",
                               inline=True)
    attendance_embed.add_field(name="Google Form Link", value=url, inline=False)
    attendance_embed.set_footer(text="Brought to you by 'The f'in Sheriff'")
    attendance_msg = await ctx.send(embed=attendance_embed)
    await attendance_msg.add_reaction(emoji)

    def attendance_react_check(reaction, user):
        return user != bot.user and str(reaction.emoji) == emoji

    while True:
        try:
            _react, _user = await bot.wait_for('reaction_add', check=attendance_react_check, timeout=120)
            await _react.remove(_user)
            db_con = sqlite3.connect("data/bot.sqlite")
            db_cur = db_con.cursor()
            db_cur.execute("SELECT * FROM user_info WHERE discordID=?", (_user.id,))
            data = db_cur.fetchone()
            db_con.close()
            if data is None:
                await _user.send("You have not verified your information. Please use !verify to do so.")
            else:
                # (discordID, email, name, studentID)
                f_name, l_name = data[1].split(" ")
                f_name_id = "entry.1253937586"
                l_name_id = "entry.690931678"
                student_id_id = "entry.1427818186"
                data = {
                    f_name_id: f_name,
                    l_name_id: l_name,
                    student_id_id: data[2],
                    "emailAddress": data[3]
                }
                params = "?"
                for key, value in data.items():
                    params += f"{key}={value}&"
                params = params[:-1]
                _url = url + params
                print(_url)
                await _user.send(f"Automatically generated filled attendance form: {_url}")
        except asyncio.TimeoutError:
            await ctx.send(f'Attendance has ended.')
            break
    # split into groups of 10


bot.run(token=_token)

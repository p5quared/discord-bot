import os
import asyncio
import json
import random

import discord
from discord.ext import commands
from discord.ext.commands import Bot
from dotenv import load_dotenv

#testing
load_dotenv()
_token = os.environ['DISCORD_TOKEN']
_intents = discord.Intents.default()
_intents.message_content = True
bot = Bot(command_prefix='$', intents=_intents)

with open("help.json", "r") as f:
    help_file = json.load(f)


def read_cache():
    with open("roles.json", "r") as f:
        roles_cache = json.load(f)
    for role in roles_cache:
        _title = roles_cache[role]['embed']['title']
        _descr = roles_cache[role]["embed"]["description"]
        roles_cache[role]["embed"] = discord.Embed(title=_title,
                                                   description=_descr)
    return roles_cache


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


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author == bot.user:
        return

    if not message.guild:
        print("DM detected.")
        await message.channel.send("DM received.")

    if "bot is bad" in message.content:
        # send threatening DM
        await message.author.send("I WILL SLAUGHTER YOUR FAMILY!!!!!!!!!!!!")

    #  sadly this does not work yet
    if message.author == "Nelson#8832":
        print("I've been waiting for you, Nelson!!!!")
    if message.author == "nathan#7654":
        print("I've been waiting for you, Nathan!!!!")


@bot.command()
async def rm(ctx, arg=None):
    """
    This function posts react-role managers.
    They must be preconfigured and are extracted from "roles.json" on bot startup.
    After the message is sent, the ID of the message is automatically cached and
    associated with the desired role from roles.json.
    Note: Calling this function twice for the same role with overwrite the previously cached ID.
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
    await target_channel.send(msg.content)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, q):
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
async def helps(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send("Here is a list of the currently implemented commands:")
    o_str = ''
    print(help_file)
    for cmd in help_file.values():
        o_str += f'Name: {cmd["name"]}\n'
        o_str += f'Usage: {cmd["usage"]}\n'
        o_str += f'Description: {cmd["description"]}\n\n'
    await ctx.send(o_str)

@bot.command()
async def release(ctx):
    await ctx.channel.purge(limit=1)
    with open("release_notes.md", "r") as f:
        notes = f.read()
    # notes = "```" + notes + "```"
    _embed = discord.Embed(title="Latest Release Notes:",
                           description=notes)
    await ctx.send(embed=_embed)


@bot.command()
async def rps(ctx):
    choices_rps = ["rock🪨", "paper🧻 ", "scissors✂️.... 👀"]
    choices_reg = ["rock", "paper", "scissors"]
    await ctx.send(f"Rock, paper, or scissors? Choose wisely...🥸")

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
            await ctx.send(f'Wouh!!! we really had to tie 🫥 .\nYour choice: {user_choice}\n my_choice: {pc_choice}')
        elif "paper" in pc_choice:
            await ctx.send(
                f"That's why I'm smarter,you can't beat me 😎 \nYour choice: {user_choice}\n my_choice: {pc_choice}")
        elif "scissors" in pc_choice:
            await ctx.send(
                f"HOLY, You must have used all your luck. Congratulations you win 🎉🥳. \nYour choice: {user_choice}\n my_choice: {pc_choice}")
    #   Let's set the condition for paper
    if user_choice == 'paper':
        if "paper" in pc_choice:
            await ctx.send(f'Wouh!!! You really wanted to settle for a draw 🫥  .\nYour choice: {user_choice}\n '
                           f'my_choice: {pc_choice}')
        elif "scissors" in pc_choice:
            await ctx.send(
                f"Welp, what can I say don't me tell you taught you had a chance 😎 \nYour choice: {user_choice}\n "
                f"my_choice: {pc_choice}")
        elif "rock" in pc_choice:
            await ctx.send(
                f"Their must have been a bugged somewhere, but Congratulations you win 🥳🎉  \nYour choice: {user_choice}\nmy_choice: {pc_choice}")
    #   Let's set the condition for scissors
    if user_choice == 'scissors':
        if "scissors" in pc_choice:
            await ctx.send(f"Unfortunately it's a tie 🫥  .\n Your choice: {user_choice}\n my_choice: {pc_choice}")
        elif "rock" in pc_choice:
            await ctx.send(f" Like we didn't already know that i would win 😎 \nYour choice: {user_choice}\n my_choice: {pc_choice}")
        elif "paper" in pc_choice:
            await ctx.send(
                f"My developer is a newbie I'll let you have this one. Congratulations you win 🥳🎉  \nYour choice: {user_choice}\nmy_choice: {pc_choice}")


bot.run(token=_token)

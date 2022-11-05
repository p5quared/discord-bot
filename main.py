import os
import asyncio
import json

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv
from bot_functions.send_message import send_message

# personal note:
# :set relativenumber
# :set number
#  from nltk.sentiment import SentimentIntensityAnalyzer

load_dotenv()
# _appID = os.environ['APP_ID']
# _guildID = os.environ['GUILD_ID']  # hmm... did I ever use this?
_token = os.environ['DISCORD_TOKEN']
# _publicKEY = os.environ['PUBLIC_KEY']
# wait a minute... did I ever use any of these???

_intents = discord.Intents.default()
_intents.message_content = True

bot = Bot(command_prefix='$', intents=_intents)

id_cache = dict()


def read_cache():
    with open("roles.json", "r") as f:
        roles_cache = json.load(f)
    print(f'roles_cache at open: {roles_cache}')
    for role in roles_cache:
        _title = roles_cache[role]['embed']['title']
        _descr = roles_cache[role]["embed"]["description"]
        roles_cache[role]["embed"] = discord.Embed(title=_title,
                                                   description=_descr)
    print(f'roles_cache after convert: {roles_cache}')
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
    if not arg:
        await ctx.send("Please enter the title of the role-reaction file.")
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
                    await member.add_roles(role_desired)
    # if payload.message_id == id_cache['ROLETEST']:
    #     member = payload.member
    #     guild = member.guild
    #     emoji = payload.emoji.name
    #     role = None
    #     if emoji == '🍌':
    #         role = discord.utils.get(guild.roles, name="Banana")
    #     elif emoji == '🌯':
    #         role = discord.utils.get(guild.roles, name="Burrito")
    #     if role is not None:
    #         await member.add_roles(role)


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
    # if payload.message_id == id_cache['ROLETEST']:
    #     guild = await(bot.fetch_guild(payload.guild_id))
    #     emoji = payload.emoji.name
    #     role = None
    #     if emoji == '🍌':
    #         role = discord.utils.get(guild.roles, name="Banana")
    #     elif emoji == '🌯':
    #         role = discord.utils.get(guild.roles, name="Burrito")
    #     if role is not None:
    #         member = await(guild.fetch_member(payload.user_id))
    #         await member.remove_roles(role)


@bot.command()
async def send(ctx):
    """
    This function should send messages to desired channels.
    :param ctx:
    :return: N/a
    """
    await send_message(ctx)


@bot.command()
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
async def tictactoe(ctx):
    pass


bot.run(token=_token)

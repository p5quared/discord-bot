import os

import discord
from discord.ext.commands import Bot
from dotenv import load_dotenv

#  from nltk.sentiment import SentimentIntensityAnalyzer

load_dotenv()
# _appID = os.environ['APP_ID']
# _guildID = os.environ['GUILD_ID']  # hmm... did I ever use this?
_token = os.environ['DISCORD_TOKEN']
# _publicKEY = os.environ['PUBLIC_KEY']
# wait a minute... did I ever use any of these???

_intents = discord.Intents.default()
_intents.message_content = True

bot = Bot(command_prefix='%', intents=_intents)


@bot.event
async def on_ready():
    print(f'Bot is logged in as {bot.user}')


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(f'MESSAGE RECEIVED:\nUSER:{message.author}\nBODY: {message.content}\n')
    if message.author == bot.user:
        print("Skipping message reply: identical user\n")
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


@bot.command(name='test')
async def test(ctx):
    await ctx.send("command recognized")


bot.run(token=_token)

#main.py
#author: Major#3577

import discord

intents = discord.Intents.default()
intents.reactions = True

from discord.ext import commands
from discord.ext.commands import bot

from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")

#Globals
vote_emojis = {"upvote": "<:upvote:708029780896907304>", "downvote": "<:downvote:708029810974130176>"}

selected_channel_id = 906024535923499058
selected_vote_percentage = 60 #%

#Bot
bot = commands.Bot(command_prefix="ddb$")
bot_id = 906035361032052756

@bot.event
async def on_ready():
    print("Downvote Delete Bot started! (Logged in as {0.user}.)".format(bot))

@bot.event
async def on_message(message):
    message_channel = message.channel
    if message_channel != bot.get_channel(selected_channel_id):
        # Message was outside of target channel, ignored
        return

    await message.add_reaction(vote_emojis["upvote"])
    await message.add_reaction(vote_emojis["downvote"])
    
@bot.event
async def on_raw_reaction_add(payload):
    reaction_channel = bot.get_channel(payload.channel_id)
    reaction_message = await reaction_channel.fetch_message(payload.message_id)
    
    if payload.channel_id != selected_channel_id:
        # Reaction was outside of target channel, ignored
        return

    if payload.user_id == bot_id:
        # Reaction was done by the bot, ignored
        return

    votes = {"upvote": 0, "downvote": 0}

    for reaction in reaction_message.reactions:
        reaction_name = reaction.emoji.name
        if reaction_name == "upvote" or reaction_name == "downvote":
            votes[reaction_name] = reaction.count


@bot.event
async def on_raw_reaction_remove(payload):
    reaction_channel = bot.get_channel(payload.channel_id)
    reaction_message = await reaction_channel.fetch_message(payload.message_id)

    if payload.channel_id != selected_channel_id:
        # Reaction was outside of target channel, ignored
        return

    votes = {"upvote": 0, "downvote": 0}

    for reaction in reaction_message.reactions:
        reaction_name = reaction.emoji.name
        if reaction_name == "upvote" or reaction_name == "downvote":
            votes[reaction_name] = reaction.count

#Token
bot.run(token)
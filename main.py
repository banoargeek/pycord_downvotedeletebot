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
reaction_votes = {"<:upvote:708029780896907304>": 0, "<:downvote:708029810974130176>": 0}

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
    
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot_id:
        # Reaction was done by the bot, ignored
        return
    
    if payload.channel_id != selected_channel_id:
        # Reaction was outside of target channel, ignored
        return

    for reaction in message.reactions:
        reaction_string = str(reaction)
        if reaction_string == reaction_votes[1] or reaction_string == reaction_votes[2]:
            votes[reaction_string] = (reaction.count) - 1

@bot.event
async def on_raw_reaction_remove(payload):
    #if payload.user_id == bot_id:
    #    # Reaction was done by the bot, ignored
    #    return
    
    if payload.channel_id != selected_channel_id:
        # Reaction was outside of target channel, ignored
        return

    for reaction in message.reactions:
        reaction_string = str(reaction)
        if reaction_string == reaction_votes[1] or reaction_string == reaction_votes[2]:
            votes[reaction_string] = (reaction.count) - 1

#Token
bot.run(token)
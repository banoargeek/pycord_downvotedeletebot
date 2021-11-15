#main.py
#author: Major#3577

#One Last Test!

import datetime
from datetime import date
from datetime import datetime

import discord

intents = discord.Intents.default()
intents.reactions = True

from dotenv import load_dotenv
from os import getenv

load_dotenv()

token = getenv("TOKEN")

#Globals
vote_emojis = {"upvote": "<:upvote:708029780896907304>", "downvote": "<:downvote:708029810974130176>"}

selected_channel_id = 906024535923499058
# - (Upvotes / Total Votes) * 100 - If percentage is less than selected, the message is removed
# - Note: in the future, the bot's vote may not found, but for now it does.
selected_vote_percentage = 25

#Bot
#bot = commands.Bot(command_prefix="ddb$")
bot = discord.Client()

@bot.event
async def on_ready():
    print(f"Downvote Delete Bot started! (Logged in as {bot.user}.)")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"(Bot last started: {date.today()} @ {datetime.now()})"))

@bot.event
async def on_message(message):
    message_channel = message.channel
    if message_channel != bot.get_channel(selected_channel_id):
        # - Message was outside of target channel, ignored
        return

    await message.add_reaction(vote_emojis["upvote"])
    await message.add_reaction(vote_emojis["downvote"])
    
@bot.event
async def on_raw_reaction_add(payload):
    reaction_channel = bot.get_channel(payload.channel_id)
    reaction_message = await reaction_channel.fetch_message(payload.message_id)
    
    if payload.channel_id != selected_channel_id:
        # - Reaction was outside of target channel, ignored
        return

    if payload.user_id == bot.user.id:
        # - Reaction was done by the bot, ignored
        return

    if reaction_message.author.id == payload.user_id:
        # - Reaction was done by the poster
        if payload.emoji == vote_emojis["upvote"]:
            # - Reaction was an upvote, removed
            await reaction_message.remove_reaction(payload.emoji, payload.user_id)

    votes = {"upvote": 0, "downvote": 0}

    for reaction in reaction_message.reactions:
        reaction_name = reaction.emoji.name
        if reaction_name == "upvote" or reaction_name == "downvote":
            votes[reaction_name] = reaction.count
    
    print("---- Bot reaction update ----")
    print(f"upvotes: {votes['upvote']}, downvotes: {votes['downvote']}")

    total_votes = votes["upvote"] + votes["downvote"]
    vote_percentage = round((votes["upvote"] / total_votes) * 100, 2)
    print(f"Vote percentage: {vote_percentage}%")

    if vote_percentage < selected_vote_percentage:
        await reaction_message.delete()

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

    print("---- Bot reaction update ----")
    print(f"upvotes: {votes['upvote']}, downvotes: {votes['downvote']}")

    total_votes = votes["upvote"] + votes["downvote"]
    vote_percentage = round((votes["upvote"] / total_votes) * 100, 2)
    print(f"Vote percentage: {vote_percentage}%")

    if vote_percentage < selected_vote_percentage:
        await reaction_message.delete()

#Token
bot.run(token)
"""ned_bot, the boi himself

Features:
    - Reacts with a "D" emoji to messages that already have "N" and "E" emojis
    - Tells people to stop swearing
"""
# External imports
import discord
import re
import yaml
# No internal imports

# Loads the yaml file
with open('bot.yml', 'r') as file:
    BOT_YAML = yaml.load(file, Loader=yaml.SafeLoader)
with open('bad_word_list.yml', 'r') as file:
    BAD_WORD_LIST = yaml.load(file, Loader=yaml.SafeLoader)
# Initializes the discord bot
NED_BOT = discord.Client()
# Prints that the bot is ready
@NED_BOT.event
async def on_ready():
    print(f'{NED_BOT.user} has connected to Discord')

# Essentially just bad code that does the second feature
@NED_BOT.event
async def on_raw_reaction_add(payload):
    # Checks if the emoji is an "E" emoji
    if payload.emoji.name == '🇪':
        # Gets the channel object from the channel id
        channel = NED_BOT.get_channel(payload.channel_id)
        # Gets the message that the reaction was made in
        message = await channel.fetch_message(payload.message_id)
        # Iterates through the reactions of the message
        for reaction in range(0, len(message.reactions)):
            # If the reaction of the emoji "N" was made
            if message.reactions[reaction].emoji == '🇳':
                # Makes sure we don't get an off by 1 error
                if reaction + 1 <= len(message.reactions):
                    # If the next emoji is an "E"
                    if message.reactions[reaction + 1].emoji == '🇪':
                        # Complete the bot's name
                        await message.add_reaction('🇩')
# Swear word checker
@NED_BOT.event
async def on_message(message):
    message_content = message.content.lower()
    for word in BAD_WORD_LIST['swearwords']:
        pattern = re.compile(word.lower())
        if pattern.search(message_content) is not None:
            channel = NED_BOT.get_channel(message.channel.id)
            await channel.send(BOT_YAML['NO_SWEAR_TEXT'])
            break

# Stores the API token and the name of the guild the bot is in
TOKEN = BOT_YAML['TOKEN']

# Runs the bot using with the API token
NED_BOT.run(TOKEN)

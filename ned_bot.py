"""ned_bot, the boi himself

Features:
    - Reacts with a "D" emoji to messages that already have "N" and "E" emojis
    - Tells people to stop swearing
"""
# External imports
import discord
import logging
import random
import re
import yaml
# No internal imports

# Setup the logger

logging.basicConfig(filename='discord.log', filemode='a', format='%(asctime)s %(message)s', level='ERROR')


# Loads the yaml file
with open('bot.yml', 'r') as file:
    BOT_YAML = yaml.load(file, Loader=yaml.SafeLoader)
with open('bad_word_list.yml', 'r') as file:
    BAD_WORD_LIST = yaml.load(file, Loader=yaml.SafeLoader)
# Flags punctuation characters
PUNCTUATION_CHARS = ["\'", '\"', '\:', '\;', '\/', '\?', '\.', '\>', '\,', '\<',
'\{', '\[', '\]', '\}', '\\', '\|', '\+', '\=', '\-', '\_', '\!', '\@', '\#',
'\$', '\%', '\^', '\&', '\*', '\(', '\)', '^', '$', '\s']

PUNCTUATION_PATTERN = f"({'|'.join(PUNCTUATION_CHARS)})"
SWEAR_WORDS_PATTERN = '|'.join(map(str.lower, BAD_WORD_LIST['swearwords']))
SWEAR_WORD_REGEX = re.compile(PUNCTUATION_PATTERN + SWEAR_WORDS_PATTERN + PUNCTUATION_PATTERN)

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
    if payload.emoji.name in ['🇪', '3️⃣']:
        # Gets the channel object from the channel id
        channel = NED_BOT.get_channel(payload.channel_id)
        # Gets the message that the reaction was made in
        message = await channel.fetch_message(payload.message_id)
        for reaction in message.reactions:
            if reaction.emoji == '🇳':
                await message.remove_reaction('🇷')
                await message.add_reaction('🇩')
                logging.error('Spelled my name :)')
                break
# Swear word checker
@NED_BOT.event
async def on_message(message):
    # Converts the message content to lowercase
    message_content = message.content.lower()
    # Doesn't check the bot's messages for swearwords
    if message.author != NED_BOT.user:
        if SWEAR_WORD_REGEX.search(message_content) is not None:
            channel = NED_BOT.get_channel(message.channel.id)
            # Use error warning level, otherwise discord.py goes gamer mode
            logging.error('Told ' + message.author.name + ' to watch their language')
            await channel.send(random.choice(BOT_YAML['NO_SWEAR_TEXT']))

# Stores the API token and the name of the guild the bot is in
TOKEN = BOT_YAML['TOKEN']

# Runs the bot using with the API token
NED_BOT.run(TOKEN)

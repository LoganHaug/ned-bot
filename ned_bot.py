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
'\$', '\%', '\^', '\&', '\*', '\(', '\)', '^', '$', ' ']
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
    if payload.emoji.name == '🇪' or payload.emoji.name == '3️⃣':
        # Gets the channel object from the channel id
        channel = NED_BOT.get_channel(payload.channel_id)
        # Gets the message that the reaction was made in
        message = await channel.fetch_message(payload.message_id)
        for reaction in message.reactions:
            if reaction.emoji == '🇳':
                await message.add_reaction('🇩')
                logging.error('Spelled my name :)')
                break
# Swear word checker
@NED_BOT.event
async def on_message(message):
    # Converts the message content to lowercase
    message_content = message.content.lower()
    # Doesn't check the bot's messages for swearwords
    if message.author.name == 'Ned' and message.author.discriminator == '7668':
        pass
    else:
        # Checks each swearword for matches within the message
        for word in BAD_WORD_LIST['swearwords']:
            # Converts the swearword example to lowercase
            punctuation_characters_group = '('
            for character in PUNCTUATION_CHARS:
                if PUNCTUATION_CHARS.index(character) != len(PUNCTUATION_CHARS) - 1:
                    punctuation_characters_group += character + '|'
                    continue
                punctuation_characters_group += character + ')'
            # Compiles the overtuned regex
            pattern = re.compile(punctuation_characters_group + word.lower() + punctuation_characters_group)
            # If the pattern matches send a message
            if pattern.search(message_content) is not None:
                channel = NED_BOT.get_channel(message.channel.id)
                # Use error warning level, otherwise discord.py goes gamer mode
                logging.error('Told ' + message.author.name + ' to watch their language')
                await channel.send(random.choice(BOT_YAML['NO_SWEAR_TEXT']))
                break

# Stores the API token and the name of the guild the bot is in
TOKEN = BOT_YAML['TOKEN']

# Runs the bot using with the API token
NED_BOT.run(TOKEN)

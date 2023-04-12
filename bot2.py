import discord, string, re, os
from dotenv import load_dotenv
from discord.ext import commands

"""
bad_words consist of the words that are prohibited
- mommy
"""
bad_words = [
    #r"m{1,}[ou0]{1,}m{1,}y", # Matches 'mommy' variations
    r"d{1,}[@a]{1,}d{1,}y"
    ]

# Import Environment Variables
load_dotenv()

# Initialize Bot Intents & Permissions
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="", intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} is online.')

@bot.event
async def on_message(message):
    # Skip if new message from bot
    if message.author.bot:
        return
    
    # Match new message from bad_words list
    if re.search(pattern="(" + ")|(".join(bad_words) + ")", string=message.content.lower().translate({ord(c): None for c in string.whitespace}), flags=re.IGNORECASE):
        await message.channel.send(f'{message.author.mention} FUCK YOU DEGENERATE SCUM. YOU WASTE OF GOVERNMENT TAX PAYER MONEY. FORTNIGHTLY PAYMENT PIECE OF SHIT GO AND MAKE SOME CONTRIBUTIONS TO SOCIETY.')

    # good/bad bot prompts
    if "good bot" in message.content.lower():
        await message.channel.send(f'<:OkayChamp:837353399124492328>')

    if "bad bot" in message.content.lower():
        await message.channel.send(f'<:donkSad:837353022145298462>')
    
    # When bot is @'d
    if bot.user.mentioned_in(message):
        await message.add_reaction(f'<:4WeirdW:837351889531437077>')

bot.run(os.getenv('BOT_TOKEN2'))
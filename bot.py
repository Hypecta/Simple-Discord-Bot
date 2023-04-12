import asyncio

import discord, string, re, os
from dotenv import load_dotenv
from discord.ext import commands

from cogs.fun import Fun

"""
bad_words consist of the words that are prohibited
- mommy/mother
"""
bad_words = [
    r"m{1,}[ou0]{1,}m{1,}[a@]{0,}y", # Matches 'mommy' variations
    r"m{1,}[ou0]{1,}th[e3]{1,}r",  # Matches 'mother' variations
    ]

# Import Environment Variables
load_dotenv()

# Initialize Bot Intents & Permissions
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# List of cogs to load
extensions = [Fun]

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
        await message.channel.send(f'<a:peepoblushshake:1050640802533093416>')

    if "bad bot" in message.content.lower():
        await message.channel.send(f'<a:Blubbers:1000378228483031162>')
    
    # When bot is @'d
    if bot.user.mentioned_in(message):
        await message.add_reaction(f'<:reallyinnocent:1094866016691036260>')

    await bot.process_commands(message)

async def main():
    for extension in extensions:
        try:
            cog = extension(bot)
            print(f"Loading {type(cog).__name__}")
            await bot.add_cog(cog)
        except Exception as e:
            print(type(e).__name__, str(e))
    await bot.start(os.getenv('BOT_TOKEN', ""))

if __name__ == "__main__":
    asyncio.run(main())

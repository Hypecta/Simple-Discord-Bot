import discord, string, re, os, asyncio, random
from dotenv import load_dotenv
from discord.ext import commands

from cogs.fun import Fun

'''bad_words consist of the words that are prohibited'''
bad_words = [
    r"m{1,}[ou0]{1,}m{1,}[a@]{0,}y", # Matches 'mommy' variations
    r"m{1,}[ou0]{1,}th[e3]{1,}r",  # Matches 'mother' variations
    ]

'''List of reaction emotes'''
good_bot_emotes = [f'<:DonkHappy:1000485972305268806>', f'<:peepoHappylove:981514778608558080>', f'<a:peepoblushshake:1050640802533093416>']

bad_bot_emotes = [f'<:donkSad:981514780365951006>', f'<a:jul:1090654116436516904>', f'<a:Blubbers:1000378228483031162>']

'''Bot Variables'''
pings = {"counter": 0, "channel": None}

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
        await message.add_reaction(random.choice(good_bot_emotes))

    if "bad bot" in message.content.lower():
        await message.add_reaction(random.choice(bad_bot_emotes))
    
    # When bot is @'d
    if bot.user.mentioned_in(message):
        pings["counter"] += 1
        if message.channel == pings["channel"]:
            if pings["counter"] > 2:
                await message.add_reaction(f'<a:pinged:1095633681852412004>')
            else:
                await message.add_reaction(f'<:reallyinnocent:1094866016691036260>')
        else:
            pings["channel"] = message.channel
            await message.add_reaction(f'<:reallyinnocent:1094866016691036260>')
    else:
        pings["counter"] = 0

    await bot.process_commands(message)

async def main():
    # Load bot extensions
    for extension in extensions:
        try:
            cog = extension(bot, bad_words)
            print(f"Loading {type(cog).__name__}")
            await bot.add_cog(cog)
        except Exception as e:
            print(type(e).__name__, str(e))
    await bot.start(os.getenv('BOT_TOKEN', ""))

if __name__ == "__main__":
    asyncio.run(main())
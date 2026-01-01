import discord
from discord.ext import commands
import re

# ---------------------- CONFIG ----------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Words the moderation bot blocks
BAD_WORDS = ["fuck", "shit", "bitch", "67", "skibidi", "ass", "nigger", "dick", "niger"]

# Channel IDs
STARTUP_CHANNEL_ID = 1455793643670732972
EXEMPT_CHANNELS = [1455632644967502000, 1455281535329505350]

# Regex to ignore custom emojis like <:name:id> or <a:name:id>
CUSTOM_EMOJI_PATTERN = re.compile(r"<a?:\w+:\d+>")

# ---------------------- EVENTS ----------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    channel = bot.get_channel(STARTUP_CHANNEL_ID)
    if channel:
        await channel.send('**Bot started. Nobody can cuss, say "67", or say "skibidi" in any of their sentences.**')

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return

    # Skip exempt channels
    if message.channel.id in EXEMPT_CHANNELS:
        await bot.process_commands(message)
        return

    # Allow messages with attachments (images/GIFs) without deleting
    if message.attachments:
        await bot.process_commands(message)
        return

    # Remove custom emojis from message before checking
    text = CUSTOM_EMOJI_PATTERN.sub("", message.content.lower())

    # Split message into words and check for bad words
    words = re.findall(r"\b\w+\b", text)
    if any(word in BAD_WORDS for word in words):
        await message.delete()

    await bot.process_commands(message)

# ---------------------- RUN BOT ----------------------
import os

bot.run(os.environ["DISCORD_TOKEN"])


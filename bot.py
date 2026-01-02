import discord
from discord.ext import commands
import re
import os
from discord.utils import escape_markdown, escape_mentions

# ---------------------- CONFIG ----------------------
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Words the moderation bot blocks
BAD_WORDS = [
    "fuck", "shit", "bitch", "67", "skibidi",
    "ass", "nigger", "dick", "niger"
]

# Channel IDs
STARTUP_CHANNEL_ID = 1456677007940259921
LOG_CHANNEL_ID = 1456677007940259921
EXEMPT_CHANNELS = [
    1455632644967502000,
    1455281535329505350
]

# Regex to ignore custom emojis like <:name:id> or <a:name:id>
CUSTOM_EMOJI_PATTERN = re.compile(r"<a?:\w+:\d+>")

# ---------------------- EVENTS ----------------------
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    channel = bot.get_channel(STARTUP_CHANNEL_ID)
    if channel:
        await channel.send("Restarted.")

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return

    # Skip exempt channels
    if message.channel.id in EXEMPT_CHANNELS:
        await bot.process_commands(message)
        return

    # Allow messages with attachments (images/GIFs)
    if message.attachments:
        await bot.process_commands(message)
        return

    # Remove custom emojis before checking
    cleaned_text = CUSTOM_EMOJI_PATTERN.sub("", message.content.lower())

    # Split into words
    words = re.findall(r"\b\w+\b", cleaned_text)

    if any(word in BAD_WORDS for word in words):
        original_content = message.content
        author = message.author
        channel_name = message.channel.mention

        try:
            await message.delete()

            log_channel = bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                safe_content = escape_mentions(
                    escape_markdown(original_content)
                )

                await log_channel.send(
                    f"Message Deleted\n"
                    f"**User:** {author}\n"
                    f"**Channel:** {channel_name}\n"
                    f"**Message:** \"{safe_content}\"",
                    silent=True
                )

        except discord.Forbidden:
            pass

    await bot.process_commands(message)

# ---------------------- RUN BOT ----------------------
import os

bot.run(os.environ["DISCORD_TOKEN"])

#bot.py

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Load our .env file
load_dotenv()

# Get the Discord token from .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up Discord permissions/intents
intents = discord.Intents.default()
intents.message_content = True

# Create the bot
bot = commands.Bot(command_prefix="!", intents=intents)


# Runs when the bot successfully connects to Discord
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# Simple test command
@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command()
async def join(ctx):
    # Check if the person using the command is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You need to join a voice channel first!")
        return

    channel = ctx.author.voice.channel

    # Connect the bot to that voice channel
    await channel.connect()

    await ctx.send(f"Joined {channel.name}!")


# Start the bot
bot.run(TOKEN)
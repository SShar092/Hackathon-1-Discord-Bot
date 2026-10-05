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


# Start the bot
bot.run(TOKEN)
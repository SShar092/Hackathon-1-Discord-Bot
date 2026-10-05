#bot.py

import os
import platform

import discord
import yt_dlp   

from discord.ext import commands
from dotenv import load_dotenv

if platform.system() == "Darwin":
    discord.opus.load_opus("/opt/homebrew/opt/opus/lib/libopus.dylib")

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

@bot.command()
async def play(ctx, *, search):
    # User must be in a voice channel
    if ctx.author.voice is None:
        await ctx.send("Join a voice channel first!")
        return

    channel = ctx.author.voice.channel

    # Connect if the bot isn't connected yet
    if ctx.voice_client is None:
        await channel.connect()

    # Don't start another song while one is already playing
    if ctx.voice_client.is_playing():
        await ctx.send("I'm already playing something!")
        return

    await ctx.send(f"Searching for: {search}")

    ydl_options = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "default_search": "ytsearch",
    }

    with yt_dlp.YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(search, download=False)

        # Searches return multiple entries, so grab the first result
        if "entries" in info:
            info = info["entries"][0]

        audio_url = info["url"]
        title = info.get("title", "Unknown song")

    if platform.system() == "Darwin":
        ffmpeg_cmd = "/opt/homebrew/bin/ffmpeg" # Mac
    else:
        ffmpeg_cmd = "ffmpeg.exe" # Windows

    source = discord.FFmpegPCMAudio(
        audio_url,
        executable= ffmpeg_cmd,
        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
    )

    ctx.voice_client.play(source)

    await ctx.send(f"Now playing: **{title}**")

@bot.command()
async def pause(ctx):
      #check if bot is in a voice channel
         if ctx.voice_client is None:
            await ctx.send("I am not conected to a voice channel!")
            return

         #check if there is currently any audio playing:
         if ctx.voice_client.is_playing():
             ctx.voice_client.pause()
             await ctx.send("The song has been paused! " \
             "To resume, type '!resume'")
         else:
             await ctx.send("⏸️There is no audio playing. ")

@bot.command()
async def resume(ctx):
        #check if bot is in a voice channel
         if ctx.voice_client is None:
            await ctx.send("I am not conected to a voice channel!")
            return
        
         #check if there is currently any audio playing:
         if ctx.voice_client.is_playing():
             await ctx.send("There is currently audio playing. ")
         else:
             ctx.voice_client.resume()
             await ctx.send("▶️Audio Resumed! ")
    
# Start the bot
bot.run(TOKEN)
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
PREFIX = os.getenv("COMMAND_PREFIX", "!")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Bot {bot.user} is online")
    await bot.change_presence(activity=discord.Game(f"พิมพ์ {PREFIX}help เพื่อดูคำสั่ง"))

@bot.event
async def setup_hook():
    await bot.load_extension("commands.covid")
    await bot.load_extension("commands.lotto")
    await bot.load_extension("commands.check_lotto")
    await bot.load_extension("commands.help")
    await bot.load_extension("commands.ping")
    await bot.load_extension("tasks.auto_lotto")

bot.run(TOKEN)
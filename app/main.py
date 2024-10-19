import logging
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
from commands.commands import medibot, meditatie
from database.database import init_db, create_tables

logging.basicConfig(level=logging.INFO)

load_dotenv()
token = os.getenv("TOKEN")
database_url = os.getenv("DATABASE_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logging.info(f'Logged on as {bot.user}!')
    bot.db_pool = init_db(database_url)
    if bot.db_pool:
        create_tables(bot.db_pool)

bot.add_command(meditatie)
bot.add_command(medibot)

bot.run(token)

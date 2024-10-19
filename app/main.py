import psycopg2
from psycopg2 import pool
import logging
import os
from discord.ext import commands
import discord
from dotenv import load_dotenv
from datetime import date

logging.basicConfig(level=logging.INFO)

load_dotenv()
token = os.getenv("TOKEN")
database_url = os.getenv("DATABASE_URL")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

db_pool = None

def init_db():
    global db_pool
    try:
        db_pool = psycopg2.pool.SimpleConnectionPool(
            1, 10, database_url
        )
        if db_pool:
            logging.info("Database connection pool created successfully.")
        else:
            logging.error("Database connection pool failed.")
    except Exception as e:
        logging.error(f"Failed to connect to the database: {e}")
        db_pool = None

def execute_query(query, params):
    conn = None
    try:
        conn = db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()
    except Exception as e:
        logging.error(f"Failed to execute query: {e}")
    finally:
        if conn:
            db_pool.putconn(conn)

def create_tables():
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS meditatii (
            id SERIAL PRIMARY KEY,
            materie VARCHAR(255),
            data DATE
        )
    '''
    execute_query(create_table_query, ())

@bot.command(name="meditatie")
async def meditatie(ctx, materie: str = None, data_meditatie: str = None):
    if not db_pool:
        await ctx.send("Nu s-a putut conecta la baza de date.")
        return

    if not materie:
        await ctx.send("Te rog să specifici materia pentru meditație.")
        return

    if not data_meditatie:
        data_meditatie = date.today().strftime("%Y-%m-%d")

    insert_query = 'INSERT INTO meditatii (materie, data) VALUES (%s, %s)'
    execute_query(insert_query, (materie, data_meditatie))
    
    await ctx.send(f'Ai adăugat o nouă meditație. Materie: {materie}. Data: {data_meditatie}.')

@bot.command(name="medibot")
async def medibot(ctx):
    help_msg = (
        "📚 **Medibot - Ghidul Comenzilor** 📚\n"
        "--------------------------------------------\n"
        "🧘‍♂️ **!meditatie [materie] [data]**\n"
        "> Adaugă o nouă meditație pentru materia specificată.\n"
        "> **Exemplu:** `!meditatie matematica 25/10/2024`\n"
        "> - Dacă data nu este specificată, se va folosi data curentă.\n"
        "> - **Exemplu fără dată:** `!meditatie fizica`\n\n"
        "🤖 **!medibot**\n"
        "> Afișează acest mesaj de ajutor, cu toate comenzile disponibile și descrierile acestora.\n\n"
        "💡 **Sfat util:**\n"
        "> Folosește aceste comenzi pentru a-ți organiza mai bine sesiunile de meditație și pentru a nu uita de ele!\n"
        "--------------------------------------------\n"
        "🔗 **Link util:** [Ghid complet pentru utilizarea Medibot](https://example.com)"
    )
    await ctx.send(help_msg)

@bot.event
async def on_ready():
    logging.info(f'Logged on as {bot.user}!')
    init_db()
    if db_pool:
        create_tables()

bot.run(token)

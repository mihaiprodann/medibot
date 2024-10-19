from discord.ext import commands
from datetime import date

@commands.command(name="meditatie")
async def meditatie(ctx, materie: str = None, data_meditatie: str = None):
    if not ctx.bot.db_pool:
        await ctx.send("Nu s-a putut conecta la baza de date.")
        return

    if not materie:
        await ctx.send("Te rog să specifici materia pentru meditație.")
        return

    if not data_meditatie:
        data_meditatie = date.today().strftime("%Y-%m-%d")

    insert_query = 'INSERT INTO meditatii (materie, data) VALUES (%s, %s)'
    
    
    conn = None
    try:
        conn = ctx.bot.db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(insert_query, (materie, data_meditatie))
        conn.commit()
        cursor.close()
        await ctx.send(f'Ai adăugat o nouă meditație. Materie: {materie}. Data: {data_meditatie}.')
    except Exception as e:
        await ctx.send("A apărut o eroare la conectarea la baza de date.")
        print(f"Database error: {e}")
    finally:
        if conn:
            ctx.bot.db_pool.putconn(conn)


@commands.command(name="medibot")
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

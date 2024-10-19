from discord.ext import commands
from datetime import date, datetime
import discord

@commands.command(name="medibot")
async def medibot(ctx):
    embed = discord.Embed(
        title="📚 Medibot - Ghidul Comenzilor 📚",
        description="Un bot pentru organizarea sesiunilor de meditație.",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="🧘‍♂️ **!meditatie [add/delete] [argumente]**",
        value=(
            "> Adaugă sau șterge o meditație pentru materia specificată.\n"
            "> **Exemplu pentru adăugare:** `!meditatie add matematica 2024-10-20`\n"
            "> - Dacă data nu este specificată, se va folosi data curentă.\n"
            "> **Exemplu pentru ștergere:** `!meditatie delete [id]`\n"
            "> - Șterge meditația cu ID-ul specificat."
        ),
        inline=False
    )

    embed.add_field(
        name="🗓 **!meditatii**",
        value=(
            "> Afișează o listă a meditațiilor tale pentru acest server, inclusiv statusul (Finalizată/Astăzi/În X zile)."
        ),
        inline=False
    )

    embed.add_field(
        name="🤖 **!medibot**",
        value="> Afișează acest mesaj de ajutor, cu toate comenzile disponibile și descrierile acestora.",
        inline=False
    )

    embed.add_field(
        name="💡 **Sfat util**",
        value="> Folosește aceste comenzi pentru a-ți organiza mai bine sesiunile de meditație și pentru a nu uita de ele!",
        inline=False
    )

    embed.set_footer(text="🔗 Ghid complet pentru utilizarea Medibot: https://example.com")

    # Optionally, you can set a thumbnail or image if you want to add the bot's logo
    embed.set_thumbnail(url="https://i.imgur.com/6sGYR0P.png")  # Make sure this URL is valid

    await ctx.send(embed=embed)




@commands.command(name="meditatii")
async def meditatii(ctx):
    if not ctx.bot.db_pool:
        await ctx.send("Nu s-a putut conecta la baza de date.")
        return

    server_id = str(ctx.guild.id)  # Get the current server's ID

    # Fetch meditations for the current server
    query = 'SELECT id, materie, data FROM meditatii WHERE server_id = %s ORDER BY data'
    conn = None
    rows = []
    
    try:
        conn = ctx.bot.db_pool.getconn()
        cursor = conn.cursor()
        cursor.execute(query, (server_id,))
        rows = cursor.fetchall()
        cursor.close()
    except Exception as e:
        await ctx.send("A apărut o eroare la interogarea bazei de date.")
        print(f"Database error: {e}")
    finally:
        if conn:
            ctx.bot.db_pool.putconn(conn)

    # If no meditations, notify the user
    if not rows:
        await ctx.send("Nu există meditații pentru acest server.")
        return

    # Prepare the table content
    today = date.today()
    message_lines = ["📅 **Lista Meditațiilor:**"]

    for med_id, materie, data_meditatie in rows:
        data_meditatie = datetime.strptime(str(data_meditatie), '%Y-%m-%d').date()

        # Determine the status
        if data_meditatie < today:
            status = "✅ Finalizată"
        elif data_meditatie == today:
            status = "📅 Astăzi"
        else:
            days_left = (data_meditatie - today).days
            status = f"⏳ În {days_left} zile"

        # Format row
        line = f"**#{med_id}** - *{materie}* - **{data_meditatie.strftime('%d/%m/%Y')}** - {status}"
        message_lines.append(line)

    # Combine all rows into a single message
    message = "\n".join(message_lines)

    # Send the result
    await ctx.send(message)


@commands.command(name="meditatie")
async def meditatie(ctx, action: str = None, *args):
    if not ctx.bot.db_pool:
        await ctx.send("Nu s-a putut conecta la baza de date.")
        return

    # Ensure action is specified
    if action not in ["add", "delete"]:
        await ctx.send("Te rog să specifici o acțiune validă: `add` sau `delete`.")
        return

    server_id = str(ctx.guild.id)  # Get the current server's ID

    # Handle "add" action
    if action == "add":
        if len(args) < 1:
            await ctx.send("Te rog să specifici materia pentru meditație.")
            return
        
        materie = args[0]
        data_meditatie = args[1] if len(args) > 1 else date.today().strftime("%d/%m/%Y")

        insert_query = 'INSERT INTO meditatii (materie, data, server_id) VALUES (%s, %s, %s)'
        
        # Insert the meditation into the database
        conn = None
        try:
            conn = ctx.bot.db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(insert_query, (materie, data_meditatie, server_id))
            conn.commit()
            cursor.close()
            await ctx.send(f'Ai adăugat o nouă meditație. Materie: {materie}, Data: {data_meditatie}.')
        except Exception as e:
            await ctx.send("A apărut o eroare la adăugarea meditației.")
            print(f"Database error: {e}")
        finally:
            if conn:
                ctx.bot.db_pool.putconn(conn)

    # Handle "delete" action
    elif action == "delete":
        if len(args) < 1:
            await ctx.send("Te rog să specifici ID-ul meditației pe care dorești să o ștergi.")
            return

        try:
            med_id = int(args[0])
        except ValueError:
            await ctx.send("ID-ul specificat nu este valid.")
            return

        delete_query = 'DELETE FROM meditatii WHERE id = %s AND server_id = %s'
        
        # Delete the meditation from the database
        conn = None
        try:
            conn = ctx.bot.db_pool.getconn()
            cursor = conn.cursor()
            cursor.execute(delete_query, (med_id, server_id))
            conn.commit()

            if cursor.rowcount > 0:
                await ctx.send(f"Meditația cu ID-ul {med_id} a fost ștearsă.")
            else:
                await ctx.send(f"Nu există nicio meditație cu ID-ul {med_id} pentru acest server.")
            cursor.close()
        except Exception as e:
            await ctx.send("A apărut o eroare la ștergerea meditației.")
            print(f"Database error: {e}")
        finally:
            if conn:
                ctx.bot.db_pool.putconn(conn)

import discord
from dotenv import load_dotenv
import os
from datetime import date

load_dotenv()
token = os.getenv("TOKEN")

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!meditatie'):
            parts = message.content.split(' ')

            bot_msg = 'Ai adăugat o nouă meditație.'

            if len(parts) > 1 and parts[1]:
                materie = parts[1]
                bot_msg += f' Materie: {materie}.'
            else:
                bot_msg += ' Nu ai setat o materie.'

            if len(parts) > 2 and parts[2]:
                data_meditatie = parts[2]
                bot_msg += f' Data: {data_meditatie}.'
            else:
                current_date = date.today().strftime("%d/%m/%Y")
                bot_msg += f' Data: {current_date}.'

            await message.channel.send(bot_msg)
        
        elif message.content.startswith('!medibot'):
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
            await message.channel.send(help_msg)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(token)

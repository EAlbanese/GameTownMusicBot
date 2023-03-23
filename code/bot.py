from asyncio import sleep
import configparser
import os
from discord import (Activity, ActivityType, ApplicationContext, Bot, Embed,
                     EmbedField, FFmpegPCMAudio, Member, Option, Permissions, Button, PartialEmoji, Game, File, Intents, utils)
import youtube_dl
import yt_dlp

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config.get('Bot', 'Token')
DEBUG_GUILDS = None if config.get('Bot', 'DebugGuilds') == "" else list(
    map(lambda id: int(id), config.get('Bot', 'DebugGuilds').split(',')))

intents = Intents.default()
intents.members = True
bot = Bot(debug_guild=DEBUG_GUILDS, intents=intents)
# db = database.Database("bot.db")
queue = []


@bot.event
async def on_ready():
    print(f'{bot.user} Music is connected')
    await bot.change_presence(activity=Activity(type=ActivityType.listening, name="Musik auf Game Town"))

# Setzt die Konfigurationsoptionen für den YoutubeDL-Wrapper
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


# Eine Funktion zum Streamen von Musik von einem YouTube-Link
def get_url(query):
    with ytdl:
        try:
            url = ytdl.extract_info(query, download=False)['url']
            return url
        except:
            return None


# Eine Funktion, um eine Audioverbindung herzustellen und Musik abzuspielen
async def play_audio(interaction: ApplicationContext, url):
    voice_channel = interaction.author.voice.channel
    vc = await voice_channel.connect()
    vc.play(FFmpegPCMAudio(url, **ffmpeg_options))
    while vc.is_playing():
        await sleep(1)
    await vc.disconnect()


# Der Bot-Befehl, um Musik abzuspielen
@bot.slash_command(description="Spiele ein Lied ab")
async def play(interaction: ApplicationContext, query):
    url = get_url(query)
    if url:
        await play_audio(interaction, url)
    else:
        await interaction.send("Konnte keinen Song finden.")


# Der Bot-Befehl, um den Bot aus dem Sprachkanal zu entfernen
@bot.slash_command(description="Stoppe den Bot")
async def stop(interaction: ApplicationContext):
    voice_client = interaction.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()


bot.run(TOKEN)
# db.connection.close()

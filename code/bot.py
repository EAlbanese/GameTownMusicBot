import configparser
import os
from discord import (ActivityType, ApplicationContext, Bot, Embed,
                     EmbedField, Member, Option, Permissions, Button, PartialEmoji, Game, File, Intents)
import youtube_dl

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
    await bot.change_presence(activity=ActivityType.listening('Musik auf Game Town'))


# @bot.command(name='play', help='Play a song from YouTube')
# async def play(ctx, url):
#     global queue
#     song = os.path.isfile('song.mp3')
#     try:
#         if song:
#             os.remove('song.mp3')
#     except PermissionError:
#         await ctx.send('Wait for the current playing music to end or use the stop command.')
#         return

#     voice_channel = discord.utils.get(
#         ctx.guild.voice_channels, name='YOUR_VOICE_CHANNEL')
#     await voice_channel.connect()
#     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'quiet': True,
#         'outtmpl': 'song.mp3',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192'
#         }]
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([url])

#     voice.play(discord.FFmpegPCMAudio('song.mp3'))


# @bot.command(name='stop', help='Stop the bot and leave the voice channel')
# async def stop(ctx):
#     voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
#     if voice.is_connected():
#         await voice.disconnect()
#     else:
#         await ctx.send('The bot is not connected to a voice channel.')


# @bot.command(name='addtoqueue', help='Add a song to the queue')
# async def addtoqueue(ctx, url):
#     global queue
#     queue.append(url)
#     await ctx.send(f'The song has been added to the queue. There are {len(queue)} songs in queue.')

bot.run(TOKEN)
# db.connection.close()

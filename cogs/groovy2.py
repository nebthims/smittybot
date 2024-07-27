import os
import requests
import json
import discord
from discord import FFmpegPCMAudio
from discord.opus import load_opus
from discord.ext import commands
import nacl
import asyncio


class TalkForMe(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(" - GROOVY 2.0: Ready!")
    self.voice_clients = {}
    discord.opus.load_opus('/usr/lib/arm-linux-gnueabihf/libopus.so.0')
    
  @commands.command()
  async def join(self, ctx):
    if not ctx.message.author.voice:
        await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
        return
    else:
        channel = ctx.message.author.voice.channel
    await channel.connect()
    
  @commands.command()
  async def leave(self, ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

  @commands.command()
  async def talkforme(self, ctx):
    # Load JSON:
    with open('data/speech.json', 'r') as file_object:
      talkers = json.load(file_object)
    # Check if we've sent this message before:
    if ctx.author.display_name in talkers:
      print("TALK FOR ME: Hey, I'm already talking for you!")
      await ctx.send(f"Hey, I'm already talking for you, {ctx.message.author.display_name}!")    
      return
    else:
      talkers.append(ctx.author.display_name)
      with open('data/speech.json', 'w') as file_object:
        json.dump(talkers, file_object)
      print("TALK FOR ME: Talking list updated. ")
      await ctx.send(f"Now talking for {ctx.message.author.display_name}.")

  @commands.command()
  async def talkstop(self, ctx):
    # Load JSON:
    with open('data/speech.json', 'r') as file_object:
      talkers = json.load(file_object)
    # Check if we've sent this message before:
    if ctx.author.display_name in talkers:
      print(f"TALK FOR ME: Removing {ctx.message.author.display_name} from the Talker list.")
      await ctx.send(f"Done! Not talking for you anymore, {ctx.message.author.display_name}!")   
      talkers.remove(ctx.author.display_name)
      with open('data/speech.json', 'w') as file_object:
        json.dump(talkers, file_object)
      return
    else:
      print("TALK FOR ME: Hey, I'm not talking for you yet! ")
      await ctx.send(f"No longer talking for {ctx.message.author.display_name}.")

  @commands.command()
  async def play(self, ctx):
    # Parse message content:
    message = ctx.message
    text = message.content.split(' ')[1]
    text = "audio/"+text.lower()+".mp3"
    voice_client = message.guild.voice_client
    options = '-vn -threads 1 -b:a 128k'
    if not os.path.exists(text):
      await ctx.send("Don't know that song! Ask Smitty to add it.")
      print(text)
    elif not voice_client:
      await ctx.send("Do /join first next time!")
      channel = ctx.message.author.voice.channel
      await channel.connect()
      try:
        voice_client.play(discord.FFmpegPCMAudio(source=text, executable='ffmpeg', options=options))
        print(f"GROOVY: Playing {text}")
      except AttributeError:
        print("Failed to play audio: AttributeError")
    else:
      try:
        voice_client.play(discord.FFmpegPCMAudio(source=text, executable='ffmpeg', options=options))
        print(f"GROOVY: Playing {text}")
      except AttributeError:
        print("Failed to play audio: AttributeError")


  @commands.command()
  async def stop(self, ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
        print("GROOVY: Stopped playing music.")
        await ctx.send("Stopped playing music.")
    else:
        print("GROOVY: Not currently playing any music.")
        await ctx.send("Not currently playing any music.")
    
    
  @commands.command()
  async def playlist(self, ctx):
    list = []
    mp3s = ""
    for f in os.listdir("./audio"):
      if f.endswith(".mp3"):
        list.append(f)
    for x in list:
      mp3s += ' '+ x
    mp3s = mp3s.replace(".mp3", ",")
    mp3s = mp3s[:-1]
    await ctx.send(f"The sounds you can play with **/play** are:\n> {mp3s}. \nMake sure you have connected the bot to a voice channel with **/join** first")
  
  def speakos(self, split_text):
    SPEECH_REGION = os.environ['SPEECH_REGION']
    SPEECH_KEY = os.environ['SPEECH_KEY']
    joined = ' '.join(split_text)
    url = f"https://{SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
    headers = {
          "Ocp-Apim-Subscription-Key": SPEECH_KEY,
          "Content-Type": "application/ssml+xml",
          "X-Microsoft-OutputFormat": "audio-16khz-128kbitrate-mono-mp3",
          "User-Agent": "curl"
    }
    data = f'''
      <speak version='1.0' xml:lang='en-AU'>
          <voice xml:lang='en-AU' xml:gender='Male' name='en-AU-KenNeural'>
              {joined}
          </voice>
      </speak>
      '''
    response = requests.post(url, headers=headers, data=data.encode('utf-8'))
    with open('temp/output.mp3', 'wb') as f:
      f.write(response.content)  
  
  @commands.command()
  async def test(self, ctx):
    self.speakos(ctx.message.content.split(' '))
    await ctx.send(file=discord.File('temp/output.mp3'))

async def setup(bot):
  await bot.add_cog(TalkForMe(bot))

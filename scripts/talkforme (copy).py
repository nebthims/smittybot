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
    print(" - TALK FOR ME: Ready!")
    
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

  @commands.Cog.listener()
  async def on_message(self, message):
    # Load JSON:
    with open('data/speech.json', 'r') as file_object:
        talkers = json.load(file_object)
    if isinstance(message.author, discord.Member):
      member = message.author
    # Check if we're talking for this bro':
    if member.display_name in talkers:
        voice_channel = member.voice
        if not voice_channel:
            await member.channel.send("You need to be in a voice channel to use this command!")
            return
        if not voice_channel.channel:
            await member.channel.send("You need to be in a voice channel to use this command!")
            return
        if message.guild.voice_client and message.guild.voice_client.is_connected():
            await member.voice.client.disconnect()
        vc = await voice_channel.channel.connect()
        print(vc)
        # Create the TTS message:
        self.speakos(message.content.split(' '))
        # Send the TTS message:
        options = '-vn -threads 1 -b:a 128k'
        await vc.play(discord.FFmpegPCMAudio(source='temp/output.mp3', executable='ffmpeg/ffmpeg', options=options))

        while vc.is_playing():
            await asyncio.sleep(1)
        await vc.disconnect()


  def speakos(self, split_text):
    SPEECH_REGION = os.environ['SPEECH_REGION']
    SPEECH_KEY = os.environ['SPEECH_KEY']
    joined = ' '.join(split_text[1:])
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
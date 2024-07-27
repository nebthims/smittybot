from discord.ext import commands
import discord
import emoji
import random
from datetime import date as dt
from scripts.poll_options import options

class Polls(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(" - POLLS: Ready!")

  #@commands.Cog.listener()   # ASIO Spyware that listens for "BroPoll"
  #async def on_message(self, message):
    #if "BROPOLL" in message.content.upper():
      #print("POLLS: BroPoll detected!")
      #split_text = message.content.split(' ')
      #react_emojis = []
      #for _ in split_text:
        #if _ in emoji.EMOJI_DATA or "<" in _:
          #react_emojis.append(_)
      #for _ in react_emojis:
        #await message.add_reaction(_)
        #print(_)

  @commands.command()
  async def poll(self, ctx):
    temp_options = options
    split_text = ctx.message.content.split(' ')
    newList = []
    reacts = []
    embed = discord.Embed(title = f"BroPoll for {dt.today()}")
    for _ in split_text[1:]:
        newList.append(_.title())
    for _ in range(len(newList)):
      random.shuffle(temp_options)
      reacts.append(temp_options.pop())
      embed.add_field(name = newList[_], value = reacts[_], inline = False)
    msg = await ctx.send(embed = embed)
    for _ in reacts:
      await msg.add_reaction(_)
      

async def setup(bot):
    await bot.add_cog(Polls(bot))

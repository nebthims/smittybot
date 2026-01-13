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
    content = ctx.message.content
    if ',' not in content:
      await ctx.send("Separate the items with commas.")
      return
    temp_options = options.copy()
    options_text = content[len('/poll '):]
    split_text = [option.strip() for option in options_text.split(',') if option.strip()]
    if not split_text:
      await ctx.send("You didn't list anything!")
      return
    reacts = []
    embed = discord.Embed(title = f"BroPoll for {dt.today()}")
    for _ in split_text:
      emoji = temp_options.pop(random.randint(0,len(temp_options)-1))
      reacts.append(emoji)
      embed.add_field(name = _.title(), value = emoji, inline = False)
    msg = await ctx.send(embed = embed)
    for _ in reacts:
      await msg.add_reaction(_)
      

async def setup(bot):
    await bot.add_cog(Polls(bot))


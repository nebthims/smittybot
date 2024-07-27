from discord.ext import commands
import json
from datetime import datetime as dt
import pytz

tz = pytz.timezone('Australia/Melbourne')

class Slurs(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(" - SLURBOT 2.0: Ready!")


  @commands.command() # /slur command
  async def slur(self, ctx):
    print("SLURBOT 2.0: ⚠️🚨 Slur Detected! 🚨⚠️")
    # Parse message content:
    text = ctx.message.content.split(' ')
    broname = text[1]
    broname = broname.upper()
    slur = ' '.join(text[2:])

    # Exception handling for alternate bronames:
    if 'SMI' in broname:
      broname = 'Smitty'
    if 'DLU' in broname or 'FALK' in broname:
      broname = 'Falkland'
    if 'LEW' in broname:
      broname = 'Lewie'
    if 'GIL' in broname:
      broname = 'Gilly'
    if 'SPY' in broname:
      broname = 'Spyrou'
    if 'COO' in broname or 'MATT' in broname or 'BEE' in broname or 'SWAG' in broname:
      broname = 'Coombs'
    if not broname:
      broname = ctx.author
    if not slur:
      slur = "???"
      
    # Handle JSON Data:
    with open('data/slurs.json', 'r') as file_object:
      slurdata = json.load(file_object)
    if broname not in slurdata:
      slurdata[broname] = 1
    else:
      slurdata[broname] += 1
    slurcounter = sum(slurdata.values())
  
    with open('data/slurs.json', 'w') as file_object:
      json.dump(slurdata, file_object)


    # Send Message
    await ctx.send('⚠️🚨 SLUR DETECTED! 🚨⚠')
    await ctx.send(f'**{broname}** was the culprit. He said **{slur}**!')
    await ctx.send(f'There have been **{str(slurcounter)}** slurs since we started counting, and {broname} is responsible for {str(slurdata[broname])} of them.')

    # Setup Channel Variables:
    last_slurrer_channel = self.bot.get_guild(114725157007917057).get_channel(
        1046393641796653076)
    last_slur_channel = self.bot.get_guild(114725157007917057).get_channel(
        1049271608382066738)
    total_slurs_channel = self.bot.get_guild(114725157007917057).get_channel(
        1046393725040996373)
    days_without_channel = self.bot.get_guild(114725157007917057).get_channel(
        1046393602928033832)
    
    # Rename Channels:
    if last_slurrer_channel.name != f"Last Slurrer: {broname}":
      await last_slurrer_channel.edit(name=f"Last Slurrer: {broname}")
      print("SLURBOT2.0: Renamed Last Slurrer Channel.")
    else:
      print("SLURBOT2.0: Didn't need to rename Last Slurrer Channel.")
    if last_slur_channel.name != f"Last Slur: {slur}":
      await last_slur_channel.edit(name=f"Last Slur: {slur}")
      print("SLURBOT2.0: Renamed Last Slur Channel.")
    else:
      print("SLURBOT2.0: Didn't need to rename Last Slur Channel.")
    await total_slurs_channel.edit(name=f"Total Slurs: {str(slurcounter)}")
    print("SLURBOT2.0: Renamed Total Slurs Channel.")
    if days_without_channel.name != "Days Without Slur: 0":
      await days_without_channel.edit(name="Days Without Slur: 0")
      print("SLURBOT2.0: Renamed Days Without Channel.")
    else:
      print("SLURBOT2.0: Didn't need to rename Days Without Channel.")

    # More JSON:
    today = str(dt.now().astimezone(tz).date())
    daydata = {"Last Slur": today}
    with open('data/days.json', 'w') as file_object2:
      json.dump(daydata, file_object2)
  
  @commands.command() # /leaderboard command
  async def leaderboard(self, ctx):
    # Handle JSON:
    with open('data/slurs.json', 'r') as file_object:
      slurdata = json.load(file_object)
    slurdata_sorted = sorted(slurdata.items(), key=lambda a: a[1])
    slurdata_bros = list(zip(*slurdata_sorted))[0]
    slurdata_count = list(zip(*slurdata_sorted))[1]
    print(slurdata_bros)
    print(slurdata_count)
      
    await ctx.send(':trophy: **The Slur Leaderboard:** :trophy:')
    await ctx.send('😀 **'+slurdata_bros[0]+'**: '+str(slurdata_count[0]))
    await ctx.send('🙂 **'+slurdata_bros[1]+'**: '+str(slurdata_count[1]))
    await ctx.send('😐 **'+slurdata_bros[2]+'**: '+str(slurdata_count[2]))
    await ctx.send('🤨 **'+slurdata_bros[3]+'**: '+str(slurdata_count[3]))
    await ctx.send('😒 **'+slurdata_bros[4]+'**: '+str(slurdata_count[4]))
    await ctx.send('😠 **'+slurdata_bros[5]+'**: '+str(slurdata_count[5]))

async def setup(bot):
    await bot.add_cog(Slurs(bot))

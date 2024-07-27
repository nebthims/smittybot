from discord.ext import commands
import discord
import random
import requests
from scripts.poll_options import options as OPTIONS
from PIL import Image, ImageDraw
from io import BytesIO
import io
import aiohttp
from scripts.grid import make_grid

brodota = ["34194037", "4862317", "34474001", "30141888", "20877084"]
async def get_heroes():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.opendota.com/api/heroes") as response:
            if response.status == 200:
                HEROES = await response.json()


class Strawpolls(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print(" - STRAWPOLLS: Ready!")

  @commands.command()
  async def strawpoll(self, ctx):
    match_dates = {}  # create an empty dictionary to store match IDs and their start times
    for _ in brodota: # find all recent bro games
        requests.post(f"https://api.opendota.com/api/players/{_}/refresh")
        response = requests.get(f"https://api.opendota.com/api/players/{_}/recentMatches")
        for x in response.json():
            try:
                match_id = x["match_id"]
                match_start_time = x["start_time"]
                match_dates[match_id] = match_start_time
            except:
                print(f"Skipping match without match_id: {x}")
                continue
    latest_match_id = max(match_dates, key=match_dates.get)
    response = requests.get(f"https://api.opendota.com/api/matches/{latest_match_id}") # find info on most recent bro game
    radiant_win = response.json()["radiant_win"]
    radiant_score = response.json()["radiant_score"]
    dire_score = response.json()["dire_score"]
    if radiant_win == True:
      winner = "Radiant Victory"
      embed_colour = 65281
    else:
      winner = "Dire Victory"
      embed_colour = 16384514
    players = {}
    all_ids = {}
    count = 0
    for x in response.json()["players"]: # get player and hero information
        count += 1
        if "personaname" in x: # figure out which team bros were on
          pname = x["personaname"]
          if pname == "Smitty" or pname == "dluX" or pname == "Gilly" or pname == "spybro":
            if x["player_slot"]<100:
              team = 1
              if radiant_win == True:
                winner = "Radiant Victory, bros won!"
              else:
                winner = "Dire Victory, bros lost."
            else:
              team = 2
              if radiant_win == True:
                winner = "Radiant Victory, bros lost."
              else:
                winner = "Dire Victory, bros won!"
        else:
          pname = "Private User"+str(count)
        heroid = x["hero_id"]
        for y in HEROES.json():
          if y["id"] == heroid:
            heroname = y["localized_name"]
        players[pname] = heroname, x["player_slot"]
        all_ids[pname] = heroid, x["player_slot"]

    if team == 1: # delete values that aren't bros
      broteam = {key: value[0] for key, value in players.items() if value[1] <= 100}
      hero_nums = {key: value[0] for key, value in all_ids.items() if value[1] <= 100}
    else:
      broteam = {key: value[0] for key, value in players.items() if value[1] >= 100}
      hero_nums = {key: value[0] for key, value in all_ids.items() if value[1] >= 100}
    hero_ids = hero_nums.values()
    
    temp_options = OPTIONS[:] # set up embed
    broList = list(broteam.keys())
    heroList = list(broteam.values())
    reacts = []
    
    embed1 = discord.Embed(title = f"Strawpoll for Dota Match {latest_match_id}", color = embed_colour)
    image_bytes = make_grid(hero_ids)
    file = discord.File(io.BytesIO(image_bytes), filename="heroes.png")
    embed1.set_image(url='attachment://heroes.png')
    link = "https://www.opendota.com/matches/"+str(latest_match_id)
    await ctx.send(file=file, embed=embed1)

    embed2 = discord.Embed(color = embed_colour)
    embed2.add_field(name = 'Result', value = winner)
    embed2.add_field(name = 'Score', value = 'Radiant: '+str(radiant_score)+', Dire: '+str(dire_score))
    if "won" in winner:
      embed2.add_field(name = "Who's a Legend??", value = '', inline = False)
    else:
      embed2.add_field(name = "Who's to Blame?", value = '', inline = False)
    for _ in range(len(broList)):
      random.shuffle(temp_options)
      reacts.append(temp_options.pop())
      embed2.add_field(name = broList[_]+" as "+heroList[_], value = reacts[_], inline = False)
    link = "https://www.opendota.com/matches/"+str(latest_match_id)
    embed2.add_field(name = '', value = '➡️ [game details]('+link+')', inline = False)
    msg = await ctx.send(embed = embed2)
    for _ in reacts:
      await msg.add_reaction(_)


async def setup(bot):
    await get_heroes()
    await bot.add_cog(Strawpolls(bot))

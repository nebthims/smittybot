import requests
import json
import random
import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw
from io import BytesIO
import io
import aiohttp
from scripts.grid import make_grid

class DotaPick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(" - DOTAPICK: Ready!")
        self.heroes = []
        self.hero_list_task = None
  
    @tasks.loop(hours=240, reconnect=True)  # Random Dota Bot - Hero List Updater
    async def hero_list(self):
      async with aiohttp.ClientSession() as session:
        async with session.get("https://api.opendota.com/api/heroes") as response:
          if response.status == 200:
            HEROES = await response.json()
      for y in range(len(HEROES)):
        if HEROES[y]["localized_name"] not in self.heroes:
          self.heroes.append(HEROES[y]["localized_name"])
        with open("data/dotaheroes.json", "w") as f:
            json.dump(self.heroes, f)
    

    @commands.command() # Random Dota Bot - Ban Command
    async def dban(self, ctx):
      bro = ctx.author.name
      text = ctx.message.content.split("/dban ")[1]  # Remove the "/dban " prefix
      lowercase_words = ["of", "the", "and", "or", "in", "to", "for", "a", "an", "at", "with", "on", "from", "by"]
      lst = []
      for string in text.split(", "):
          substrings = [substring.strip() for substring in string.split(" ")]
          new_substrings = []
          for i, substring in enumerate(substrings):
              if i == 0:
                  new_substrings.append(substring.capitalize())
              elif substring.lower() in lowercase_words:
                  new_substrings.append(substring.lower())
              else:
                  new_substrings.append(substring.capitalize())
          lst.append(" ".join(new_substrings))
      # Load JSON:
      with open('data/bans.json', 'r') as f:
          bans = json.load(f)
      if bro not in bans:
          bans[bro] = []
      for hero in lst:
          if hero in self.heroes and hero not in bans[bro]:
              bans[bro].append(hero)
      await ctx.send(f"{bro} successfully banned {', '.join(lst)}!")
      with open('data/bans.json', 'w') as f:
        json.dump(bans, f)

    @commands.command() # Random Dota Bot - UnBan Command
    async def dunban(self, ctx):
      bro = ctx.author.name
      text = ctx.message.content.split("/dunban ")[1]  # Remove the "/dunban " prefix
      lowercase_words = ["of", "the", "and", "or", "in", "to", "for", "a", "an", "at", "with", "on", "from", "by"]
      lst = []
      for string in text.split(", "):
          substrings = [substring.strip() for substring in string.split(" ")]
          new_substrings = []
          for i, substring in enumerate(substrings):
              if i == 0:
                  new_substrings.append(substring.capitalize())
              elif substring.lower() in lowercase_words:
                  new_substrings.append(substring.lower())
              else:
                  new_substrings.append(substring.capitalize())
          lst.append(" ".join(new_substrings))
      with open('data/bans.json', 'r') as f:
          bans = json.load(f)
      if bro not in bans:
          bans[bro] = []
      for hero in lst:
          if hero in self.heroes and hero in bans[bro]:
              bans[bro].remove(hero)
          elif hero not in bans[bro]:
            await ctx.send(f"{ctx.author.mention}, you haven't banned {hero}! Use /dlist to see who you've banned.")
            return
      await ctx.send(f"{bro} successfully unbanned {lst}!")
      with open('data/bans.json', 'w') as f:
          json.dump(bans, f)

    @commands.command() # Random Dota Bot - BanList Command
    async def dlist(self, ctx):
      bro = ctx.author.name
      # Load JSON:
      with open('data/bans.json', 'r') as f:
        bans = json.load(f)
      if bro not in bans:
          await ctx.send("You haven't banned anyone yet!")
      else:
        await ctx.send(f"{bro}'s list of banned heroes:")
        await ctx.send(bans[bro])

    @commands.command() # Random Dota Bot - Random Command
    async def drandom(self, ctx):
      bro = ctx.author.name
      if "ban" in ctx.message.content:
        text = ctx.message.content.split("/drandom ")[1]
      else:
        text = None
      # Load JSON:
      with open('data/bans.json', 'r') as f:
        bans = json.load(f)
      brobans = bans[bro]
      if text == "ban":
        options = set(brobans)
      else:
        options = set(self.heroes) - set(brobans)
      choice = random.choice(list(options))
      await ctx.send(f"{ctx.author.mention}, you should pick **{choice}**!")



    @commands.command() # Random Dota Bot - Get a random successful Dota2 team from a recent pro game
    async def dteam(self, ctx):
      # Get a recent random pro game:
      HEROES = requests.get("https://api.opendota.com/api/heroes")
      data = requests.get("https://api.opendota.com/api/proMatches")
      choice = random.randint(0,9)
      match = data.json()[choice]["match_id"]
      print(f"Match ID: {match}")
      response = requests.get(f"https://api.opendota.com/api/matches/{match}") 
      data = response.json()
      players = data["players"]
      radiant_win = response.json()["radiant_win"]
      radiant_score = response.json()["radiant_score"]
      dire_score = response.json()["dire_score"]
      borked = False
      if "lane_role" not in data:
        borked = True
      if radiant_win == True:
        winner = "Radiant Victory"
        embed_colour = 65281
      else:
        winner = "Dire Victory"
        embed_colour = 16384514
      
      # Create a dictionary to hold the players and their corresponding heroes
      player_dict = {}
      for player in players:
          if player["isRadiant"] == data["radiant_win"]:
              if "lane_role" in player:
                  lane_role = player["lane_role"]
              else:
                if not borked:  
                  lane_role = "Support"
                else:
                  lane_role = "?"
              hero_id = player["hero_id"]
              player_dict[player["player_slot"]] = {
                  "hero_id": hero_id,
                  "lane_role": lane_role
                  }
      
      # Sort the players by their core role (position 1, 2, or 3)
      sorted_players = sorted(player_dict.values(), key=lambda x: x["lane_role"])
      hero_ids = []
      for player in sorted_players:
          hero_id = player["hero_id"]
          hero_ids.append(hero_id)
      
      # Print the list of players and which hero they played as a Discord embed:
      embed1 = discord.Embed(title="Here's a recent Pro game:", color=embed_colour)
      image_bytes = make_grid(hero_ids)
      file = discord.File(io.BytesIO(image_bytes), filename="heroes.png")
      embed1.set_image(url='attachment://heroes.png')
      await ctx.send(file=file, embed=embed1)

      embed2 = discord.Embed(color=embed_colour)
      embed2.add_field(name='Result', value=winner)
      embed2.add_field(name='Score', value='Radiant: ' + str(radiant_score) + ', Dire: ' + str(dire_score))
      position_count = 1
      for player in sorted_players:
          hero_id = player["hero_id"]
          for y in HEROES.json():
              if y["id"] == hero_id:
                  hero_name = y["localized_name"]
          lane_role = player["lane_role"]
          if lane_role == "Support":
              embed2.add_field(name="", value=f"Support: {hero_name}", inline=False)
          else:
              embed2.add_field(name="", value=f"{position_count}. {hero_name}", inline=False)
              position_count += 1
      link = "https://www.opendota.com/matches/"+str(match)
      embed2.add_field(name = '', value = '➡️ [game details]('+link+')', inline = False)
      await ctx.send(embed=embed2)

async def setup(bot):
    dota_cog = DotaPick(bot)
    await bot.add_cog(dota_cog)
    dota_cog.hero_list_task = dota_cog.hero_list.start()

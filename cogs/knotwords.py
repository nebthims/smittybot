import discord
from discord.ext import commands
import json

class Knotwords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.classic_scores = {}
        self.mini_scores = {}
        print(" - KNOTWORDS: Ready!")

    @commands.Cog.listener()  
    async def on_message(self, message):
        if message.channel.id == 934690017924763689:
          # Check if the message is a Knotwords Daily Classic or Mini message
          if "Knotwords Daily Classic" in message.content:
            game_type = "Classic"
          elif "Knotwords Daily Mini" in message.content:
            game_type = "Mini"
          else:
            return
          # Extract the user and score from the message
          user = message.author.name
          lines = message.content.split("\n")
          score = lines[1]

          # Load the score data from the JSON file
          with open("data/knots.json", 'r') as f:
            data = json.load(f)
  
          # Add the user and score to the corresponding dictionary
          data[game_type][user] = score
  
          # Print the updated scores for debugging
          print(data)
  
          with open("data/knots.json", "w") as f:
            json.dump(data, f)
  
async def setup(bot):
  await bot.add_cog(Knotwords(bot))

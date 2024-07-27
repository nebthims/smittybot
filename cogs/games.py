import discord
from discord.ext import commands
import json
import random

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        print(" - GAMES: Ready!")

    @commands.command()
    async def poolbros(self, ctx, *mentions: discord.Member):
      self.players = list(set([member.id for member in mentions]))
      await ctx.send(f"Registered players: {', '.join([member.name for member in mentions])}")
      
    @commands.command()
    async def startpool(self, ctx):
      if not self.players:
        await ctx.send("No players! Use /poolbros and mention bros to get started.")
        return
      ball_numbers = list(range(1,16))
      random.shuffle(ball_numbers)
      
      for player_id, ball_number in zip(self.players, ball_numbers):
        player = await self.bot.fetch_user(player_id)
        if player:
          try:
            await player.send(f"Your Secret Pool number for this game is **{ball_number}**!")
          except discord.Forbidden:
            await ctx.send(f"Couldn't message {player.name}. They should check their Discord DM settings.")
        else:
          await ctx.send(f"Player with ID {player_id} not found.")
  
async def setup(bot):
  await bot.add_cog(Games(bot))

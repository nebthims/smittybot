import discord
import json
from discord.ext import commands

class BroCustoms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.customs = []
        print(' - BROCUSTOMS: Ready!')

    @commands.command()
    async def newcustom(self, ctx):
      with open('data/customs.json') as f:
        self.customs = json.load(f)
      text = ctx.message.content
      split_text = text.split(" ")
      text = " ".join(split_text[2:])
      command = split_text[1]
      new_command = {
        "command": command,
        "text": text
      }
      self.customs.append(new_command)
      with open('data/customs.json', 'w') as f:
        json.dump(self.customs, f)
      await ctx.send(text)

    @commands.command()
    async def list(self, ctx):
        embed = discord.Embed(title = 'The Big List of Custom Bro Commands')
        with open('data/customs.json') as f:
          self.customs = json.load(f)
        for index in range(len(self.customs)):
          embed.add_field(name = '/'+str(self.customs[index]['command']), value = self.customs[index]['text'], inline = False)
        await ctx.send(embed = embed)

async def setup(bot):
    await bot.add_cog(BroCustoms(bot))

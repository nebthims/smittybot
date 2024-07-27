import json
with open('data/customs.json') as f:
    customs = json.load(f)

def createCog():
  f = open("cogs/brocustoms.py", "w")
  f.write("import discord\n")
  f.write("import json\n")
  f.write("from discord.ext import commands\n")
  f.write("\n")
  
  f.write("class BroCustoms(commands.Cog):\n")
  f.write("    def __init__(self, bot):\n")
  f.write("        self.bot = bot\n")
  f.write("        self.customs = []\n")
  f.write("        print(' - BROCUSTOMS: Ready!')\n")
  f.write("\n")
  f.write("    @commands.command()\n")
  f.write("    async def newcustom(self, ctx):\n")
  f.write("      with open('data/customs.json') as f:\n")
  f.write("        self.customs = json.load(f)\n")
  f.write('      text = ctx.message.content\n')
  f.write('      split_text = text.split(" ")\n')
  f.write('      text = " ".join(split_text[2:])\n')
  f.write('      command = split_text[1]\n')
  f.write('      new_command = {\n')
  f.write('        "command": command,\n')
  f.write('        "text": text\n')
  f.write('      }\n')
  f.write('      self.customs.append(new_command)\n')
  f.write("      with open('data/customs.json', 'w') as f:\n")
  f.write("        json.dump(self.customs, f)\n")
  f.write("      await ctx.send(text)\n")
  f.write("\n")
  
  for custom in customs:
    command = custom['command']
    text = custom['text']
    f.write("    @commands.command()\n")
    f.write(f"    async def {command}(self, ctx):\n")
    f.write(f'        await ctx.send("{text}")\n')
    f.write("\n")

  f.write("    @commands.command()\n")
  f.write("    async def list(self, ctx):\n")
  f.write("        embed = discord.Embed(title = 'The Big List of Custom Bro Commands')\n")
  f.write("        with open('data/customs.json') as f:\n")
  f.write("          self.customs = json.load(f)\n")
  f.write("        for index in range(len(self.customs)):\n")
  f.write("          embed.add_field(name = '/'+str(self.customs[index]['command']), value = self.customs[index]['text'], inline = False)\n")
  f.write('        await ctx.send(embed = embed)\n')
  f.write("\n")
  
  f.write("async def setup(bot):\n")
  f.write("    await bot.add_cog(BroCustoms(bot))\n")
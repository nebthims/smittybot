import os
import random
import discord
import discord.ext
from discord.ext import commands
import requests
from scripts.presences import presences
from scripts.customcog import createCog


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.messages = True

global presences

choice = random.choice(presences)
activity = discord.Game(name=choice)

bot = commands.Bot(command_prefix='/', intents=intents, activity=activity)

async def load_cogs():
  for f in os.listdir("./cogs"):
  	if f.endswith(".py"):
  		await bot.load_extension("cogs." + f[:-3])

async def unload_cogs():
  for f in os.listdir("./cogs"):
  	if f.endswith(".py"):
  		await bot.unload_extension("cogs." + f[:-3])

@bot.event # When the bot signs in:
async def on_ready():
  print("\n***---*** SmittyBot 2.0 Rebooting ***---***\n")
  print(f"Discord Username: {bot.user}\n")
  createCog()
  print("Loading all cogs from ./cogs:")
  await load_cogs()


@bot.command() # Reload Cogs
async def load(ctx):
  await unload_cogs()
  createCog()
  print("\n***---*** SmittyBot 2.0 Rebooting ***---***\n")
  print("Loading all cogs from ./cogs:")
  await load_cogs()
  await ctx.send("Successfully reloaded all Cogs!")

my_secret = os.environ["DISCORD_LOGIN"] # Discord Login Details for Bot:
try:
  bot.run(my_secret)

except:
  x = requests.get("https://discord.com/api/v6/928617838040719390", headers={"Authorization": my_secret})
  print(x)
  os.system("kill 1")

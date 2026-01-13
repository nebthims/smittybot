import discord
from discord.ext import commands, tasks
import json
from datetime import datetime, timedelta
import random

deck_list = [
    {"name": "Red Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/2/24/Red_Deck.png"},
    {"name": "Blue Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/2/24/Blue_Deck.png"},
    {"name": "Yellow Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/d/d7/Yellow_Deck.png"},
    {"name": "Green Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/1/12/Green_Deck.png"},
    {"name": "Black Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/2/20/Black_Deck.png"},
    {"name": "Magic Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/c/c3/Magic_Deck.png"},
    {"name": "Nebula Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/1/12/Nebula_Deck.png"},
    {"name": "Ghost Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/a/a1/Ghost_Deck.png"},
    {"name": "Abandoned Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/d/de/Abandoned_Deck.png"},
    {"name": "Checkered Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/a/a8/Checkered_Deck.png"},
    {"name": "Zodiac Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/2/20/Zodiac_Deck.png"},
    {"name": "Painted Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/8/8a/Painted_Deck.png"},
    {"name": "Anaglyph Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/a/ac/Anaglyph_Deck.png"},
    {"name": "Plasma Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/3/3c/Plasma_Deck.png"},
    {"name": "Erratic Deck", "image": "https://static.wikia.nocookie.net/balatrogame/images/1/17/Erratic_Deck.png"},
]

seed_list = [
    "PUSSY2", "2K9H9HN", "BRONANA", "V14NKYRB", "SLAPPY", "MZB33MVX", "BROMASS", "VMDK4RF8", "3CHAINR", "61TP3FV9", "THEBURY", "7LB2WVPK", "TOWRCUK", "D37IYHIA"
]

def generate_tournament_data():
    seed_word = random.choice(seed_list)
    deck = random.choice(deck_list)
    return seed_word, deck

async def post_tournament(self):
	channel = self.bot.get_channel(self.channel)  # Replace with your channel ID
	if channel:
		# Generate data
		seed_word, deck = generate_tournament_data()
		now = datetime.now()
		current_date = now.strftime("%Y-%m-%d")
		finishing_date = (now + timedelta(days=6)).strftime("%Y-%m-%d")
				
		# Create the embed
		embed = discord.Embed(
			title=f"Biweekly Balatro for {current_date}",
			description=(
				f"**Seed:** {seed_word}\n"
				f"**Deck:** {deck['name']}"
			),
			color=discord.Color.gold()
		)
		embed.set_author(
			name="Jimbo the Joker",
			icon_url="https://cdn2.steamgriddb.com/icon_thumb/62415c82dd6c47e714f473f9b0475e62.png"
		)
		embed.set_image(url=deck['image'])
		embed.set_footer(text=f"Round ends on: {finishing_date}")

		# Send the embed
		await channel.send(embed=embed)

class Balatro(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.channel = 1310805614619922563
		self.start_date = datetime(2024, 11, 24, 9, 0, 0)
		print(" - BALATRO: Ready!")

	def cog_unload(self):
		self.tournament_task.cancel()

	@tasks.loop(hours=1, reconnect=True)  # Check every hour
	async def tournament_task(self):
		# Set the timezone
		tz = pytz.timezone('Australia/Melbourne')
		now = datetime.now(tz)

		# Check if it's 9 AM and a multiple of 4 days from the start date
		elapsed_days = (now.date() - self.start_date.date()).days
		if now.hour == 9 and elapsed_days % 7 == 0:
			await post_tournament(self)
	
	@commands.command()
	async def balatronow(self, ctx):
		await post_tournament(self)

  
async def setup(bot):
  await bot.add_cog(Balatro(bot))


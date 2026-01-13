import discord
from discord.ext import commands

class Random (commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		print(" - RANDOM: Ready!")
        
	@commands.command()
	async def fix(self, ctx):
		channel = self.bot.get_channel(638516806021021757)
		message = await channel.fetch_message(1310570896439640074)
		
		for reaction in message.reactions:
			await message.add_reaction(reaction.emoji)
			
		await ctx.send("Reactions have been added!")

async def setup(bot):
	await bot.add_cog(Random(bot))

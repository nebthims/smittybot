import discord
from discord.ext import commands
import time
import subprocess
import json
import os


class Tests(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.start_time = time.time()
		print(" - TESTS: Ready!")
        
	@commands.command()
	async def stats(self,ctx):
		temp = get_pi_temperature()
		await ctx.send(f"Bot CPU Temperature: **{temp}°C**")
		elapsed_time = time.time() - self.start_time
		hours, remainder = divmod(elapsed_time, 3600)
		minutes, seconds = divmod(remainder, 60)
		await ctx.send(f"Bot Uptime: **{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds**")
		json = get_vnstat_json_output()
		usage = extract_data(json)
		await ctx.send("Bot's Internet Usage in the last 5 minutes:")
		await ctx.send(f"Upload: **{int(usage[0][0])}** bytes, Download: **{int(usage[0][1])}** bytes")
		
	@commands.command()
	async def net(self,ctx):
		json = get_vnstat_json_output()
		usage = extract_data(json)
		await ctx.send("Bot's Internet Usage in the last 5 minutes:")
		await ctx.send(f"Upload: **{int(usage[0][0])}** bytes, Download: **{int(usage[0][1])}** bytes")
		await ctx.send("Bot's Internet Usage Today:")
		await ctx.send(f"Upload: **{int(usage[1][0])}** bytes, Download: **{int(usage[1][1])}** bytes")
		await ctx.send("Bot's Internet Usage this Month:")
		await ctx.send(f"Upload: **{int(usage[2][0])}** bytes, Download: **{int(usage[2][1])}** bytes")	
	

def get_vnstat_json_output():
    """
    Runs the vnstat command with JSON output option and returns the result.
    """
    try:
        # Run the vnstat command with JSON output
        result = subprocess.run(['vnstat', '--json'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the command was executed successfully
        if result.returncode != 0:
            print("Error in executing vnstat: ", result.stderr)
            return None

        # Parse the JSON output
        json_data = json.loads(result.stdout)
        return json_data

    except FileNotFoundError:
        print("vnstat not found. Please ensure it is installed and in your PATH.")
        return None
    except json.JSONDecodeError:
        print("Error in parsing vnstat JSON output.")
        return None

def extract_data(vnstat_data):
    try:
        # Assuming the first interface is the one we're interested in
        interface_data = vnstat_data['interfaces'][0]

        # Last 5 minutes data
        last_5_minutes = [interface_data['traffic']['fiveminute'][-1]['tx'],interface_data['traffic']['fiveminute'][-1]['rx']]

        # Last day data
        last_day = [interface_data['traffic']['day'][-1]['tx'],interface_data['traffic']['day'][-1]['rx']]

        # Total for the current month
        total_month = [interface_data['traffic']['month'][-1]['tx'],interface_data['traffic']['month'][-1]['rx']]

        return last_5_minutes, last_day, total_month

    except (IndexError, KeyError):
        print("Error in parsing data. Please check the structure of the JSON file.")
        return None, None, None

def get_pi_temperature():
	try:
		with open('/sys/class/thermal/thermal_zone0/temp', 'r') as file:
			temp_str = file.read()
			# Convert from millidegree Celsius to degree Celsius
			temp_celsius = int(temp_str) / 1000.0
			return temp_celsius
	except IOError as e:
		print(f"Error reading temperature: {e}")
		return None

async def setup(bot):
    await bot.add_cog(Tests(bot))

from discord.ext import commands, tasks
import discord
import json
import random
import pytz
from datetime import datetime as dt
from scripts.presences import presences

choice = random.choice(presences)
activity = discord.Game(name=choice)


class Tasks(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.days_without_task = None
    self.presence_task = None
    self.update_knots_task = None
    self.birthday_reminder_task = None
    print(" - TASKS: Ready!")

  def __unload(self, bot):
    if self.days_without_task:
      self.days_without_task.cancel()
    if self.presence_task:
      self.presence_task.cancel()
    if self.update_knots_task:
      self.update_knots_task.cancel()
    if self.birthday_reminder:
      self.birthday_reminder.cancel()

  @tasks.loop(hours=1, reconnect=True)  # SlurBot - Updating "Days Since"
  async def update_days_without(self):
    # Get the number of days, in order to update the channel name:
    days_without_channel = self.bot.get_guild(114725157007917057).get_channel(
      1046393602928033832)
    with open('data/days.json', 'r') as file_object2:
      daydata = json.load(file_object2)
    last = str(daydata["Last Slur"])
    last_object = dt.strptime(last, '%Y-%m-%d').date()
    tz = pytz.timezone('Australia/Melbourne')

    # Check the time; if it's between 12 and 1, update the channel.
    print("\n***---***\n")
    today = dt.now().astimezone(tz).date()
    days = (today - last_object).days
    if days_without_channel.name != f"Days Without Slur: {days}":
      await days_without_channel.edit(name="Days Without Slur: " + str(days))
      print(f"TASK - Slurbot Updater: Successfully updated Channel Name - it has been {days} days without a slur.")
    else:
      print(f"TASK - Slurbot Updater: Day hasn't changed yet! It has still only been {days} days without a slur.")
    print("Timestamp: " + str(dt.now().astimezone(tz)))

  @tasks.loop(hours=8, reconnect=True)  # Update Bot Presence
  async def update_presence(self):
    tz = pytz.timezone('Australia/Melbourne')
    choice = random.choice(presences)
    await self.bot.change_presence(activity=discord.Game(name=choice))
    print("\n***---***\n")
    print(f"TASK - Presence Updater: Successfully changed bot presence to: \n\n'Playing {str(choice)}'\n")
    print(f"Timestamp: {str(dt.now().astimezone(tz))}\n")

  def get_emoji(self, rank: int) -> str:
    if rank == 0:
        return '🥇'
    elif rank == 1:
        return '🥈'
    elif rank == 2:
        return '🥉'
    else:
        return '🏅'

  @tasks.loop(hours=1, reconnect=True) # Knotwords - Automatic Leaderboard Embed Post
  async def update_knots(self):
    # Load the score data from the JSON file
    with open("data/knots.json", 'r') as f:
      data = json.load(f)
    tz = pytz.timezone('Australia/Melbourne')
    hour = dt.now().astimezone(tz).hour
    print("\n***---***\n")
    if hour == 23 and len(data["Classic"]) > 0: 
      print("TASK - Knotwords Leaderboard: Organising Leaderboard!")
      # Get today's date in the format we need
      today = dt.now().strftime("%B %d %Y")
      
      # Create the embed
      classic_embed = discord.Embed(title=f"Knotwords Daily Classic Leaderboard for {today}:")
      mini_embed = discord.Embed(title=f"Knotwords Daily Mini Leaderboard for {today}:")

      # Load the medal data from the JSON file
      with open("data/medals.json", 'r') as f:
        medals = json.load(f)
  
      # Sort the classic and mini dictionaries by their scores
      sorted_classic = sorted(data['Classic'].items(), key=lambda x: x[1])
      sorted_mini = sorted(data['Mini'].items(), key=lambda x: x[1])
  
      # Add the sorted scores to the embeds
      for i, (user, score) in enumerate(sorted_classic):
        emoji = self.get_emoji(i)
        classic_embed.add_field(name=f"{emoji} {user}", value=score, inline=False)
        if user not in medals:
          medals[user] = {"🥇": 0, "🥈": 0, "🥉": 0}
  
      for i, (user, score) in enumerate(sorted_mini):
        emoji = self.get_emoji(i)
        mini_embed.add_field(name=f"{emoji} {user}", value=score, inline=False)
        if user not in medals:
          medals[user] = {"🥇": 0, "🥈": 0, "🥉": 0}

      # Assign medals for each user
      for i, (name, time) in enumerate(sorted_classic[:3]):
          emoji = self.get_emoji(i)
          medals[name][emoji] += 1
      
      for i, (name, time) in enumerate(sorted_mini[:3]):
          emoji = self.get_emoji(i)
          medals[name][emoji] += 1

      # Send the embed
      channel = self.bot.get_channel(934690017924763689)
      await channel.send(embed=classic_embed)
      await channel.send(embed=mini_embed)

      # Save medals data to a separate JSON file
      with open('data/medals.json', 'w') as f:
          json.dump(medals, f)
  
      # Clear the data in the JSON file
      data = {"Classic": {}, "Mini": {}}
      with open("data/knots.json", 'w') as f:
          json.dump(data, f)
    else:
      print("TASK - Knotwords Leaderboard: It's not 11pm, we're still taking responses!")
    print(f"Timestamp: {str(dt.now().astimezone(tz))}\n")

  @tasks.loop(hours=1, reconnect=True) #Birthdays - Check JSON and message users
  async def birthday_reminder(self):
    tz = pytz.timezone('Australia/Melbourne')
    now = dt.now(tz)
    if now.hour == 9:
        # Load our birthdays data
        with open("data/birthdays.json") as f:
            birthdays = json.load(f)
        bdayboy = None
        for username, data in birthdays.items():
            bday_str = data["Birthday"]
            user_id = data["User ID"]
            bday = dt.strptime(bday_str, "%m-%d-%Y")
            # Check if today is the user's birthday
            if (bday.day == now.day) and (bday.month == now.month):
                bdayboy = await self.bot.fetch_user(int(user_id))
                bdayboy_name = username
                break

        if bdayboy:
            print(f"BIRTHDAYBOY - It's {bdayboy_name}'s birthday today! Messaging the bros.")
            for username, data in birthdays.items():
                user_id = data["User ID"]
                if user_id != bdayboy.id:  # we don't want to notify the birthday boy
                    user = await self.bot.fetch_user(int(user_id))
                    if user:
                        await user.send(f"It's {bdayboy_name}'s birthday today!")
        else:
            print("BIRTHDAYBOY - Nobody's birthday today")
  
async def setup(bot):
  tasks_cog = Tasks(bot)
  await bot.add_cog(tasks_cog)
  tasks_cog.days_without_task = tasks_cog.update_days_without.start()
  tasks_cog.presence_task = tasks_cog.update_presence.start()
  #tasks_cog.update_knots_task = tasks_cog.update_knots.start()
  tasks_cog.birthday_reminder = tasks_cog.birthday_reminder.start()

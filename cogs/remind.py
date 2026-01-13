
from discord.ext import commands, tasks
import asyncio
import datetime
import json
import os
import re
import discord

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reminders = []
        self.load_reminders()
        self.reminder_loop.start()
        print(" - REMINDERS: Ready!")

    def cog_unload(self):
        self.reminder_loop.cancel()
        self.save_reminders()

    def load_reminders(self):
        if os.path.exists("reminders.json"):
            with open("reminders.json", "r") as f:
                self.reminders = json.load(f)

    def save_reminders(self):
        with open("reminders.json", "w") as f:
            json.dump(self.reminders, f, indent=4)

    def parse_time(self, timestring: str) -> datetime.timedelta:
        time_regex = re.compile(r"(\d+)(s|m|h|d|w|mo|y)")
        matches = time_regex.findall(timestring.lower())
        if not matches:
            raise ValueError("Invalid time format.")

        total_seconds = 0
        for value, unit in matches:
            value = int(value)
            if unit == 's':
                total_seconds += value
            elif unit == 'm':
                total_seconds += value * 60
            elif unit == 'h':
                total_seconds += value * 60 * 60
            elif unit == 'd':
                total_seconds += value * 60 * 60 * 24
            elif unit == 'w':
                total_seconds += value * 60 * 60 * 24 * 7
            elif unit == 'mo':
                total_seconds += value * 60 * 60 * 24 * 30
            elif unit == 'y':
                total_seconds += value * 60 * 60 * 24 * 365

        return datetime.timedelta(seconds=total_seconds)

    @commands.command(name="remindme")
    async def remind_me(self, ctx, time: str, *, message: str):
        """Set a reminder. Time formats: 1y2mo3w4d5h6m7s"""
        try:
            delta = self.parse_time(time)
        except ValueError:
            await ctx.send("❌ Invalid time format. Example: `1h30m`, `2d`, `1w`, `1y2mo`")
            return

        remind_time = (datetime.datetime.utcnow() + delta).isoformat()
        reminder = {
            "user_id": ctx.author.id,
            "channel_id": ctx.channel.id,
            "time": remind_time,
            "message": message
        }
        self.reminders.append(reminder)
        self.save_reminders()

        await ctx.send(f"⏰ Reminder set for {time} from now: `{message}`")

    @tasks.loop(seconds=30)
    async def reminder_loop(self):
        now = datetime.datetime.utcnow()
        to_remove = []

        for reminder in self.reminders:
            remind_time = datetime.datetime.fromisoformat(reminder["time"])
            if now >= remind_time:
                user = self.bot.get_user(reminder["user_id"])
                if user is None:
                    try:
                        user = await self.bot.fetch_user(reminder["user_id"])
                    except (discord.NotFound, discord.HTTPException):
                        user = None

                channel = self.bot.get_channel(reminder["channel_id"])
                if channel:
                    mention_text = f"{user.mention}" if user else "someone"
                    await channel.send(f"⏰ Hey {mention_text}, reminder: **{reminder['message']}**")

                to_remove.append(reminder)

        for reminder in to_remove:
            self.reminders.remove(reminder)

        if to_remove:
            self.save_reminders()

    @reminder_loop.before_loop
    async def before_reminder_loop(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Reminder(bot))

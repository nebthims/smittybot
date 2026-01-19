import discord
from discord.ext import commands
import json
from pathlib import Path

class DailyGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.classic_scores = {}
        self.mini_scores = {}
        print(" - DAILY GAMES: Ready!")

    @commands.command(name="dumpdailygames")
    async def dump_daily_games(self, ctx):
        """Archive CluesBySam and Minute Cryptic posts from the daily channel."""
        channel_id = 934690017924763689
        channel = self.bot.get_channel(channel_id) or await self.bot.fetch_channel(channel_id)
        if channel is None:
            await ctx.send("Daily games channel not found.")
            return

        clues_messages = []
        minute_messages = []
        async for message in channel.history(limit=None, oldest_first=True):
            content = message.content or ""
            if "#CluesBySam" in content:
                clues_messages.append({
                    "Timestamp": message.created_at.isoformat(),
                    "Bro": message.author.name,
                    "Message": content,
                })
            if "Minute Cryptic" in content:
                minute_messages.append({
                    "Timestamp": message.created_at.isoformat(),
                    "Bro": message.author.name,
                    "Message": content,
                })

        data_dir = Path("data")
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "clues_by_sam.json").write_text(json.dumps(clues_messages, indent=2))
        (data_dir / "minute_cryptic.json").write_text(json.dumps(minute_messages, indent=2))

        await ctx.send(
            f"Archived {len(clues_messages)} CluesBySam and {len(minute_messages)} Minute Cryptic messages."
        )



async def setup(bot):
    await bot.add_cog(DailyGames(bot))


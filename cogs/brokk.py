import json
import random
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime

class Brokk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(" - BROKK: Ready!")

    @commands.command()
    async def brokk(self, interaction: discord.Interaction):
        current_year = str(datetime.now().year)
        prev_year = str(datetime.now().year - 1)

        # Load data
        with open("data/brokk.json", "r") as f:
            brokk = json.load(f)

        names = list(brokk.keys())
        assignments_made = False

        for name, data in brokk.items():
            user_id = int(data["User ID"])

            # Already assigned this year → just message
            if current_year in data:
                assigned_name = data[current_year]
            else:
                invalid = {name}

                if prev_year in data:
                    invalid.add(data[prev_year])

                choices = [n for n in names if n not in invalid]

                if not choices:
                    await interaction.followup.send(
                        f"❌ No valid assignment possible for {name}.",
                    )
                    return

                assigned_name = random.choice(choices)
                data[current_year] = assigned_name
                assignments_made = True

            # DM the user
            user = await self.bot.fetch_user(user_id)
            if user:
                await user.send(
                    f"🎁 **BroKK {current_year}** 🎁\n"
                    f"You have been assigned: **{assigned_name}**\n"
                    f"The spending limit is **$50**"
                    f"Schedule your gifts for **January 9th** at **6pm**\n"
                )

        # Persist changes if we made any
        if assignments_made:
            with open("data/brokk.json", "w") as f:
                json.dump(brokk, f, indent=4)

        await interaction.followup.send(
            f"✅ Brokk {current_year} assignments processed.",
            ephemeral=True
        )


async def setup(bot):
    await bot.add_cog(Brokk(bot))

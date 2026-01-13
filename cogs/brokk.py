import json
import random
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime


def generate_unique_assignments(brokk, current_year, prev_year):
    """Return a dict mapping giver -> receiver ensuring uniqueness per run.

    Respects any existing assignment for `current_year` and forbids self-gifts
    and repeat of last year's recipient. Raises ValueError if impossible.
    """
    names = list(brokk.keys())

    # Respect fixed assignments already present
    fixed = {
        name: data[current_year]
        for name, data in brokk.items()
        if current_year in data
    }

    # Detect conflicts in preexisting assignments
    if len(set(fixed.values())) != len(fixed.values()):
        raise ValueError("Conflicting fixed assignments for current year")

    remaining_targets = set(names) - set(fixed.values())
    unassigned = []
    invalids = {}

    for name, data in brokk.items():
        if name in fixed:
            continue
        inv = {name}
        if prev_year in data:
            inv.add(data[prev_year])
        invalids[name] = inv
        unassigned.append(name)

    def backtrack(order, assigned, targets_left):
        if not order:
            return assigned.copy()

        # Heuristic: pick the giver with fewest valid targets
        best = None
        best_opts = None
        for giver in order:
            opts = [t for t in targets_left if t not in invalids[giver]]
            if not opts:
                return None
            if best is None or len(opts) < len(best_opts):
                best = giver
                best_opts = opts

        giver = best
        for target in random.sample(best_opts, len(best_opts)):
            assigned[giver] = target
            new_targets = targets_left - {target}
            new_order = [g for g in order if g != giver]
            res = backtrack(new_order, assigned, new_targets)
            if res is not None:
                return res
            del assigned[giver]

        return None

    result = backtrack(unassigned, {}, remaining_targets)
    if result is None:
        raise ValueError("No valid unique assignment found")

    merged = fixed.copy()
    merged.update(result)
    return merged

class Brokk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(" - BROKK: Ready!")

    @commands.command()
    async def brokk(self, ctx: commands.Context):
        current_year = str(datetime.now().year)
        prev_year = str(datetime.now().year - 1)

        # Load data
        with open("data/brokk.json", "r") as f:
            brokk = json.load(f)

        assignments_made = False

        try:
            assignments = generate_unique_assignments(brokk, current_year, prev_year)
        except ValueError as e:
            await ctx.send(f"❌ {e}")
            return

        # Apply assignments (preserve any that were already present)
        for name, data in brokk.items():
            user_id = int(data["User ID"])
            assigned_name = assignments[name]
            if current_year not in data:
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

        await ctx.send(
            f"✅ Brokk {current_year} assignments processed."
        )

    @commands.command(name="brokk_test")
    async def brokk_test(self, ctx: commands.Context):
        """Proof-of-concept: compute assignments and print to console."""
        current_year = str(datetime.now().year)
        prev_year = str(datetime.now().year - 1)

        with open("data/brokk.json", "r") as f:
            brokk = json.load(f)

        try:
            assignments = generate_unique_assignments(brokk, current_year, prev_year)
        except ValueError as e:
            await ctx.send(f"❌ {e}")
            return

        print("Brokk test assignments:")
        for giver, receiver in assignments.items():
            print(f"{giver} -> {receiver}")

        await ctx.send(
            "✅ Brokk test completed (assignments printed to console).",
        )


async def setup(bot):
    await bot.add_cog(Brokk(bot))

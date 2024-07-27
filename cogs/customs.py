import random
import discord
from discord.ext import commands
import requests
import asyncio
import random
import datetime
import time
import typing

class Customs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(" - CUSTOMS: Ready!")
    
    @commands.command()
    async def altright(self, ctx):
        await ctx.send("https://i.imgur.com/5iZUmEK.png ")
      
    @commands.command()
    async def brotrayal(self, ctx):
        await ctx.send("Days since Brotrayal: 0")
      
    @commands.command()
    async def coombs(self, ctx):
        await ctx.send("https://i.imgur.com/eswDivO.png")
      
    @commands.command()
    async def cummies(self, ctx):
        await ctx.send("Just me and my :two_hearts:Smitty:two_hearts:, hanging out I got pretty hungry:eggplant: so I started to pout :disappointed: He asked if I was down :arrow_down:for something yummy :heart_eyes::eggplant: and I asked what and he said he'd give me his :sweat_drops:cummies!:sweat_drops: Yeah! Yeah!:two_hearts::sweat_drops: I drink them!:sweat_drops: I slurp them!:sweat_drops: I swallow them whole:sweat_drops: :heart_eyes: It makes :cupid:Smitty:cupid: :blush:happy:blush: so it's my only goal... :two_hearts::sweat_drops::tired_face:Harder Smitty! Harder Smitty! :tired_face::sweat_drops::two_hearts: 1 cummy:sweat_drops:, 2 cummy:sweat_drops::sweat_drops:, 3 cummy:sweat_drops::sweat_drops::sweat_drops:, 4:sweat_drops::sweat_drops::sweat_drops::sweat_drops: I'm :cupid:Smitty's:cupid: :crown:princess :crown:but I'm also a whore! :heart_decoration: He makes me feel squishy:heartpulse:!He makes me feel good:purple_heart: ! :cupid::cupid::cupid: He makes me feel everything a neet boy should!~ :cupid::cupid::cupid: :crown::sweat_drops::cupid:Wa-what!:cupid::sweat_drops::crown:")

    @commands.command()
    async def diablo(self,ctx):
      embed = discord.Embed(description = "Please! Deckard Cain needs your help! To break the worldstone shards he needs the three ancient numbers of power behind your [credit card](https://diabloimmortal.blizzard.com/en-gb/)!", color = 16742003)
      embed.set_author(name = "Deckard Cain", icon_url = "https://bnetcmsus-a.akamaihd.net/cms/content_folder_media/L2ISTH46LTUR1523389280900.png")
      await ctx.send(embed = embed)

    @commands.command()
    async def falk(self,ctx):
      await ctx.send(":champagne: For our Falk-len bro, Sam :champagne:")

    @commands.command()
    async def fallbros(self,ctx):
      await ctx.send("https://cdn.discordapp.com/attachments/114725157007917057/1085449190991216640/171229_human_fall_flat_3.jpg")

    @commands.command()
    async def ff14(self, ctx):
      embed = discord.Embed(description = "Did you know that the critically acclaimed MMORPG Final Fantasy XIV has a free trial, and includes the entirety of A Realm Reborn AND the award-winning Heavensward expansion up to level 60 with no restrictions on playtime? Sign up, and enjoy Eorzea today! https://secure.square-enix.com/account/app/svc/ffxivregister?lng=en-gb ", color = 5951477)
      embed.set_author(name = "Yoshi P", icon_url = "https://www.pcgamesn.com/wp-content/sites/pcgamesn/2022/06/naoki-yoshida-talks-ffxiv-accessibility.jpg")
      embed.set_image(url = "https://i.kym-cdn.com/photos/images/original/002/146/436/9aa.gif")
      await ctx.send(embed = embed)

    @commands.command()
    async def gamer(self,ctx):
      await ctx.send("https://cdn.discordapp.com/attachments/163839434377134082/872447821255704616/heated_gamer_moment.PNG")

    @commands.command()
    async def gilly(self, ctx):
      await ctx.send(":grapes: Who else remembers when Gilly played games with bros and would ask bros if they wanted to play games like rockos :grapes:")

    @commands.command()
    async def hook(self, ctx):
      api_url = "https://steamcommunity.com/market/priceoverview/?country=AU&currency=21&appid=570&market_hash_name=Dragonclaw%20Hook" 
      response = requests.get(api_url)
      cost = response.json()["median_price"]
      await ctx.send(f"The **Dragonclaw Hook** from Dota2 is currently priced at **{cost}**. \nGilly sold the hook that bros bought him for $972.22. They paid $82.52.")

    @commands.command()
    async def void(self, ctx):
      api_url = "https://steamcommunity.com/market/priceoverview/?country=AU&currency=21&appid=570&market_hash_name=Elder%20Timebreaker" 
      response = requests.get(api_url)
      cost = response.json()["median_price"]
      gains = float(cost.replace('A$ ', ''))-169.86
      await ctx.send(f"Smitty's **Elder Timebreaker** from Dota2 is currently priced at **{cost}**! \nIt's an investment, because he bought it for $169.86, on September 1st, 2014.  He's up **${gains}**!")

    @commands.command()
    async def hype(self, ctx):
      await ctx.send("WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!! WE WANT HYPE!! WE WANT SMITTY!!")

    @commands.command()
    async def liar(self, ctx):
      await ctx.send("https://i.imgur.com/kzEpHlK.png")

    @commands.command()
    async def lies(self, ctx):
      await ctx.send("https://i.imgur.com/pe9cqGZ.jpg")

    @commands.command()
    async def pray(self, ctx):
      await ctx.send(":pray:  Our Smitty, Who art haven't had covid, hallowed be Thy name; Thy cough come; Thy cough never went. Give us this day our daily meds; and stop us our cough as we hope those who cough near us don't have covid; and lead us not to get covid again, but deliver us to healthy days. :pray:")

    @commands.command()
    async def ricko(self, ctx):
      await ctx.send(":champagne: For our fallen bro, Shea :champagne:")

    @commands.command()
    async def smitty(self, ctx):
      await ctx.send("WE WANT MODERATION!! TWO GAMES WITH SMITTY!!")

    @commands.command()
    async def sadsmitty(self, ctx):
      await ctx.send("https://i.imgur.com/pMIKyC1.png?1")

    @commands.command()
    async def spybro(self, ctx):
      await ctx.send("Spybro is too busy doing dungeons with his new panda bros to talk to bros or hang out in voice https://i.imgur.com/1HSv7GC.png")

    @commands.command()
    async def weallwon(self, ctx):
      await ctx.send("https://i.imgur.com/9A26cDj.jpg")

    @commands.command()
    async def whitepower(self, ctx):
      await ctx.send("https://i.imgur.com/8nzkFsU.png")


    @commands.command()
    async def inspiration(self, ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/1067286936663891998/1085522231175688252/Smitty_333495612.png")
        await ctx.send("He might be on the spectrum...")
        await ctx.send("But it's **OUR** spectrum.")
        await ctx.send(" - Gilly Tzu")

    @commands.command()
    async def patientriki(self,ctx):
        await ctx.send("https://cdn.discordapp.com/attachments/261772275601113089/1110194423305871480/image.png")
        await ctx.send("never forget that the source of this collapse in trust and faith was caused by a little Riki that couldn't wait 4 seconds to team fight\nand that bros will be forever changed by this\n22/05/23")
      
    @commands.command() #choose command
    async def choose(self, ctx):
      text = ctx.message.content
      text = text.replace('/choose ', '')
      split_text = text.split(', ')
      choicenum = random.randint(0,len(split_text)-1)
      your_choice = split_text[choicenum]
      await ctx.send("You should pick **"+str(your_choice)+"**!")

    @commands.command() #dice roller
    async def roll(self, ctx):
      text = ctx.message.content
      text = text.replace ('/roll', '')
      if text == '':
        text = 6
      text = int(text)

      choicenum = random.randint(1,text)
      await ctx.send(f"You rolled **{str(choicenum)}** on a {text}-sided die!")
      
    @commands.command() #dice roller
    async def secretroll(self, ctx):
      text = ctx.message.content
      text = text.replace ('/secretroll', '')
      if text == '':
        text = 6
      text = int(text)

      choicenum = random.randint(1,text)
      await ctx.author.send(f"You rolled **{str(choicenum)}** on a {text}-sided die!")


    @commands.command() #dc private message
    async def dc(self, ctx):
      user = ctx.message.author
      choicenum = random.randint(10,30)
      await user.send(f'Your DC for your next check is **{str(choicenum)}**')
      
      
    @commands.command() #cummies price check
    async def cummies(self,ctx):
      api_url = "https://api.coingecko.com/api/v3/coins/cumrocket?localization=false&market_data=true" 
      response = requests.get(api_url)
      data = response.json()
      price = data["market_data"]["current_price"]["aud"]
      # Given data
      initial_price_AUD = 0.0585577  # Initial price per CumRocket coin in AUD
      coins_bought = 20151.05739775  # Total CumRocket coins bought
      coins_per_bro = coins_bought / 6  # Coins shared among six bros
      current_worth_per_bro_AUD = round(coins_per_bro * price,3)
      percent_increase = round(((price - initial_price_AUD) / initial_price_AUD) * 100,2)
      cummies_meme_message = f":sweat_drops: :rocket: **CumRocket Meme Report** :rocket: :sweat_drops:\n**CUMMIES** are currently worth **A${price}**. \n\nOn the 6th of November, 2021, we bought **{coins_bought}** CUMMIES.\nWe paid **${initial_price_AUD}** per CUMMY, for a total of $1180, after fees, at a cost of roughly **$196.65** per bro (that's **3,358.51** CUMMIES per bro).\n\nToday, that investment is worth **A${current_worth_per_bro_AUD}** per bro, an increase of **{percent_increase}%**!"
      await ctx.send(cummies_meme_message)
      await asyncio.sleep(5)
      await ctx.send(":sweat_drops: :rocket: ||<:Desmittge:1159800255831883836>||")
      
      
    @commands.command() #cummies summary - the cummary, if you will.
    async def cummary(self,ctx):
      api_url = "https://api.coingecko.com/api/v3/coins/cumrocket?localization=false&market_data=true" 
      response = requests.get(api_url)
      data = response.json()
      price = data["market_data"]["current_price"]["aud"]
      # Given data
      initial_price_AUD = 0.0585577  # Initial price per CumRocket coin in AUD
      coins_bought = 20151.05739775  # Total CumRocket coins bought
      coins_per_bro = coins_bought / 6  # Coins shared among six bros
      current_worth_per_bro_AUD = round(coins_per_bro * price,3)
      percent_increase = round(((price - initial_price_AUD) / initial_price_AUD) * 100,2)
      await ctx.send(f"Each bro owns ${current_worth_per_bro_AUD} worth of CUMMIES, an increase of {percent_increase}%")
      await ctx.send(":sweat_drops: :rocket: ||<:Desmittge:1159800255831883836>||")
        
    
    @commands.command() #the #shea command - how long since a bro was around?
    async def sheatimer(self, ctx):
      message = discord.


    @commands.command()
    async def timer(self, ctx, minutes: typing.Optional[int] = None):
        start_time = time.time()  # Record the time when the command is invoked
        
        if minutes is not None:
            timer = minutes * 60  # Convert minutes to seconds
        else:
            timer = random.randint(12, 36) * 10
    
        # Create the initial embed
        m, s = divmod(timer, 60)
        h, m = divmod(m, 60)
        time_remaining = f'{m:02d}:{s:02d}'
        embed = discord.Embed(title="Timer", description=f"Time Remaining: {time_remaining}")
        message = await ctx.send(embed=embed)
    
        # Update the embed every second
        while timer > 0:
            await asyncio.sleep(1)
            elapsed_time = time.time() - start_time  # Calculate the elapsed time
            time_left = timer - int(elapsed_time)  # Calculate the time left
            if time_left <= 0:  # Break out of the loop if time is up
                break
            m, s = divmod(time_left, 60)
            h, m = divmod(m, 60)
            time_remaining = f'{m:02d}:{s:02d}'
            embed.description = f"Time Remaining: {time_remaining}"
            await message.edit(embed=embed)
    
        # Timer is complete, update the embed with the total time waited
        m, s = divmod(timer, 60)
        h, m = divmod(m, 60)
        embed.title = f"Timer - waited {m:02d}:{s:02d}"
        embed.description = "Time's up!"
        await message.edit(embed=embed)
      
        # Message the user to let them know:
        await ctx.send(f"{ctx.author.mention}, your {m:02d}:{s:02d} timer is up!")

async def setup(bot):
    await bot.add_cog(Customs(bot))

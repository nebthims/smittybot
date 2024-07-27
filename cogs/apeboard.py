import discord
from discord.ext import commands
import json
from datetime import datetime
import pytz
import asyncio

class Apeboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print(" - APEBOARD: Ready!")
    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload): 
      apechannel = self.bot.get_guild(114725157007917057).get_channel(1065847963307495514) #Specific Channel for my server
      if (payload.emoji.name == 'broNobo'): #Specific emoji
        tz = pytz.timezone('Australia/Melbourne')
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        link = message.jump_url
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji)
        
        async for user in reaction.users():
          reactor = user
          break
        reactor_name = reactor.name.title()
        print(f"APEBOARD: Reaction Detected! {reactor_name} submitted this.")
        
        if reaction and reaction.count >= 0:
          # Load JSON:
          with open('data/apes.json', 'r') as file_object3:
            apedata = json.load(file_object3)
            
          # Check if we've sent this message before:
          if payload.message_id in apedata:
            print("APEBOARD: Hey, we've seen this message before! I'm not doing nothing.")
            return
          else:
            apedata.append(payload.message_id)
            with open('data/apes.json', 'w') as file_object3:
              json.dump(apedata, file_object3)
            print("APEBOARD: JSON Updated. ")
          
          #Set Author's Username for Embed:
          author = reaction.message.author.name          
          colourdict = {
            "beef_nuggets": 15844367,
            ".smitty": 16711680,
            "lewie": 5763719,
            "dlux": 3447003,
            "gilly91": 16020735,
            "spybro": 8846079,}
          colour = colourdict[author]
    
          # Setup Embed:
          embed = discord.Embed(description = reaction.message.content, color = colour)
          embed.set_author(name = author, icon_url = reaction.message.author.avatar)
          embed.add_field(name = '', value = '➡️ [original message]('+link+')', inline = False)
    
          # If there's an attachment: 
          if len(reaction.message.attachments) > 0:
            embed.add_field(name = '', value = '📎 [image.png]('+reaction.message.attachments[0].url+')')
            embed.set_image(url = reaction.message.attachments[0].url)
          embed.set_footer(text = f" 🐒  # {reaction.message.channel.name} | Submitted by:  {reactor_name}")
          embed.timestamp = datetime.now(tz)  
    
          # Send Embed:
          await apechannel.send(embed = embed)
          print("APEBOARD: Message sent. ")

async def setup(bot):
    try:
        await bot.add_cog(Apeboard(bot))
    except Exception as e:
        print(f"Failed to load cog: {e}")

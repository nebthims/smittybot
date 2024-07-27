import requests
import discord
from discord.ext import commands, tasks
from PIL import Image, ImageDraw
from io import BytesIO

def make_grid(hero_ids):
  output_file = 'temp/heroes.png'
  HEROES = requests.get("https://api.opendota.com/api/heroes")
  # Define grid parameters
  grid_width = 59 * len(hero_ids)
  grid_height = 33
  grid_spacing = 2
    
  # Create canvas image
  canvas = Image.new('RGBA', (grid_width + (grid_spacing * (len(hero_ids) - 1)), grid_height))
    
  # Loop through hero IDs
  for i, hero_id in enumerate(hero_ids):
    # Get hero name from HEROES.json()
    hero_name = None
    for hero in HEROES.json():
      if hero["id"] == hero_id:
        hero_name = hero["name"][14:] + "_sb"
        break
    if hero_name is None:
      raise ValueError(f"Invalid hero ID {hero_id}")
    # Download hero image
    hero_image_url = f"https://cdn.dota2.com/apps/dota2/images/heroes/{hero_name}.png"
    response = requests.get(hero_image_url)
    hero_image = Image.open(BytesIO(response.content)).convert('RGBA')
    # Calculate position on canvas
    x = i * (59 + grid_spacing)
    y = 0
    # Paste hero image onto canvas
    canvas.paste(hero_image, (x, y))
    img_buffer = BytesIO()
    canvas.save(img_buffer, format="PNG")
    img_buffer.seek(0)
    
  # Create discord file object from PNG bytes
  canvas.save(output_file, format='PNG')

  return img_buffer.getvalue()

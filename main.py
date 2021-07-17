import asyncio
from inspect import EndOfBlock
from logging import Manager, error, info
from operator import pos
from typing import ContextManager
import discord
import random
from datetime import datetime
from discord import colour
from discord import message
from discord import channel
from discord import user
from discord import member
from discord import role
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import command
from discord.ext.commands.errors import CheckFailure, MissingPermissions, MissingRequiredArgument, CommandNotFound
from discord.utils import get
import time
import os
import json
import PIL

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

bot = commands.Bot(command_prefix='>',case_insensitive=True)
bot.remove_command('help')


#on_ready event
@bot.event
async def on_ready():
    guilds = bot.guilds
    await bot.change_presence(status = discord.Status.idle, activity = discord.Activity(type=discord.ActivityType.watching, name=">help"))
    print('Bot is ready')

@bot.command()
@commands.is_owner()
async def unload(ctx, *, name: str):
    try:
        bot.unload_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send(f'"**{name}**" Cog unloaded')

#load commmand
@bot.command()
@commands.is_owner()
async def load(ctx, *, name: str):
    try:
        bot.load_extension(f"cogs.{name}")
    except Exception as e:
        return await ctx.send(e)
    await ctx.send(f'"**{name}**" Cog loaded')

#on_command_error error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command is invalid")
        return
        
    raise error

#wanted command
@bot.command()
async def wanted(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    
    wanted = Image.open("wanted.jpg")
    asset = user.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    pfp = pfp.resize((245,306))
    wanted.paste(pfp, (192,259))
    wanted.save("wan.jpg")
    await ctx.send(file=discord.File("wan.jpg"))

@bot.command()
async def delete(ctx, user: discord.Member = None):
  if user == None:
    await ctx.send('Who are you deleting dumbo?')
  
  else:
    wanted = Image.open("dele.png")
    ok = user.avatar_url_as(size=128)
    data = BytesIO(await ok.read())
    pfp = Image.open(data)
    pfp = pfp.resize((83,105))
    wanted.paste(pfp, (81,75))
    wanted.save("dele.png")
    await ctx.send(file=discord.File("dele.png"))
    await ctx.send(f'Are you sure you want to delete {user.name}? [yes or no] ')
    try:
      yoo = await bot.wait_for(
        "message",
        timeout = 30,
        check = lambda message: message.author == ctx.author
        and message.channel == ctx.channel)
      if yoo:
        if yoo.content == "yes":
          await ctx.send(f'Windows 10: {user.name} was succesfully moved to the recycle bin.')
          
        elif yoo.content == 'no':
          await ctx.send(f'Windows 10: {user.name} was not deleted.')
          
        else:
          await ctx.send('That is not a valid answer is it?')
    except asyncio.TimeoutError:
      await ctx.send("Sorry you didn't reply in time")


for file in os.listdir("cogs"): # lists all the cog files inside the cog folder.
    if file.endswith(".py"): # It gets all the cogs that ends with a ".py".
        name = file[:-3] # It gets the name of the  removing the ".py"
        bot.load_extension(f"cogs.{name}") # This loads the cog





token = os.environ.get("TOKEN")
bot.run(os.getenv("TOKEN"))
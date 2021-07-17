import asyncio
from keep_alive import keep_alive
from inspect import EndOfBlock
from logging import Manager, error, info
from operator import pos
from typing import ContextManager
import discord
import random
from datetime import datetime
from discord import message
from discord.embeds import Embed
from discord.ext import commands
from discord.ext.commands.core import command
from discord.ext.commands.errors import CheckFailure, MissingPermissions, MissingRequiredArgument, CommandNotFound
from discord.utils import get
import time
import json
import translate
from translate import Translator

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener() # You use commands.Cog.listener() instead of bot.event
    async def on_ready(self):
        print("Misc Cog is Ready!")

    @commands.command()
    async def avatar(self, ctx, user: discord.Member = None):
      if user is None:
        em = discord.Embed(title =f"Your avatar!", color = ctx.author.color)
        em.set_image(url = ctx.author.avatar_url)
        await ctx.send(embed = em)
      if user is not None:
        em = discord.Embed(title = f"{user.name}'s avatar", color = user.color)
        em.set_image(url = user.avatar_url)
        await ctx.send(embed = em)

    @commands.command()
    async def userinfo(self, ctx, member:discord.Member = None ):


      if member == None:
        top_role = ctx.author.top_role.mention 
        time = str(ctx.author.created_at)
        embed = discord.Embed(title=f"{ctx.author.name}", description =f"{ctx.author.mention}",  colour = 0xFF5733)   
        embed.add_field(name=f"Top role", value=f"{top_role}", inline = False)   
        embed.add_field(name="ID", value=f"{ctx.author.id}", inline=True)
        embed.set_thumbnail(url = ctx.author.avatar_url)
        embed.set_footer(text=f"Requested by  {ctx.author.name}")
        embed.add_field(name="Creation time", value=f"{time[0:10]}", inline=False)
        await ctx.send(embed=embed)
      
      elif member is not None:
        top_role = member.top_role.mention 
        time = str(member.created_at)
        embed = discord.Embed(title=f"{member.name}", description =f"{member.mention}",  colour = 0xFF5733)   
        embed.add_field(name=f"Top role", value=f"{top_role}", inline = False)   
        embed.add_field(name="ID", value=f"{member.id}", inline=True)
        embed.set_thumbnail(url = member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by  {ctx.author.name}")
        embed.add_field(name="Creation time", value=f"{time[0:10]}", inline=False)
        await ctx.send(embed=embed)
      




    @commands.command()
    async def serverinfo(self, ctx):
      name = ctx.guild.name
      description = ctx.guild.description

      owner = ctx.guild.owner_id
      id = ctx.guild.id
      region = ctx.guild.region
      membercount = ctx.guild.member_count

      icon = str(ctx.guild.icon_url)

      embed = discord.Embed(title = f"{name}:", description = f"{description}", colour = 0xFF5733)
      embed.add_field(name = f"ID:", value=f"{id}", inline=False)
      embed.add_field(name = f"Owner:", value = f"<@!{owner}>", inline=False)
      embed.add_field(name = f"Region:", value = f"{region}", inline=False)
      embed.add_field(name = f"Members:", value = f"{membercount}", inline=False)
      embed.set_thumbnail(url = f"{icon}")

      await ctx.send(embed=embed)

    @commands.command()
    async def translate(self, ctx,*, message):

      meat = await ctx.send("What language do you want to translate to?")
      try:
            yoo = await self.bot.wait_for(
                "message",
                timeout = 30,
                check = lambda message: message.author == ctx.author
                               and message.channel == ctx.channel
                  
                )
            translator= Translator(to_lang=f"{yoo.content}")
            translation = translator.translate(f"{message}")
            await ctx.send(translation)
            await asyncio.sleep(1)
            await yoo.delete()
            await ctx.message.delete()
            await meat.delete()
      except asyncio.TimeoutError:
        await ctx.send("Sorry, you didn't reply in time!")

    @translate.error
    async def translate_error(self, ctx, error):
      await ctx.send("That language is invalid!")

def setup(bot):
  bot.add_cog(ExampleCog(bot))

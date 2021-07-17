
import asyncio
from keep_alive import keep_alive
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


class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

		#on_ready event
    @commands.Cog.listener() # You use commands.Cog.listener() instead of bot.event
    async def on_ready(self):
        print("Help Cog is Ready!")

    #info command revaped
    @commands.command()
    async def info(self, ctx):
      embed = discord.Embed(title = 'Info about the bot.', description = 'Friends Official Bot is a bot coded in python, for specially this server!', color = ctx.author.color, url = 'https://github.com/Detroit2/Friends' )

      embed.add_field(name = 'Contributors:', value = 'Atom#6785 | GaLLanTADITYA#6600 | Vansh#6666', inline = True)

      embed.add_field(name = 'The source code is available on Github!', value = 'https://github.com/Detroit2/Friends',  inline = False)

      embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/859300990687903744/860206477049856000/a_1d9e78f79c0c6613f593f8ed08ae2927-1.png')

      embed.set_footer(text = f"Requested by {ctx.author.name}")

      embed.timestamp = datetime.utcnow()

      await ctx.send(embed = embed)


		
    #Help command group
    @commands.group(name = "help", invoke_without_command = True)
    async def help_command(self, ctx):
      embed = discord.Embed(title = "Help menu for this bot!", color = ctx.author.color)

      embed.add_field(name = "Moderation commands", value = "``>modhelp``", inline = False)

      embed.add_field(name = "Fun commands", value = "``>funhelp``", inline = False)

      embed.add_field(name = "miscellaneous commands", value = "``>mischelp``", inline = False)

      embed.set_footer(text = f"Requested by {ctx.author.name}")
      embed.timestamp = datetime.utcnow()
      await ctx.send(embed = embed)
    
    #mod help command under help group
    @help_command.command(name = 'mod')
    async def mod_help(self, ctx):
      embed = discord.Embed(title = "Moderation commands (Prefix: `>`)", color=ctx.author.color)

      embed.add_field(name = "Ban a member", value = "``>ban (member) (reason)``", inline = False)

      embed.add_field(name = "Kick a member", value = "``>kick (member) (reason)``", inline = False)

      embed.add_field(name = "Warn a member", value = "``>warn (member) (reason)``", inline = False)

      embed.add_field(name = "Check warns of a member", value = "``>warns (member)``", inline = False)

      embed.add_field(name = "Remove warning of a member", value = "``>remove (member) (id)``", inline = False)

      embed.add_field(name = "Remove all the warnings from every member in the server", value = "``>clearwarns``", inline = False)

      embed.add_field(name = 'Mute a member', value = '``>mute (member) (time and unit)``', inline = False)

      embed.add_field(name = 'Unmute a member', value = '``>unmute (user)``', inline = False)

      embed.add_field(name = 'Change slowmode of a channel', value = '``>slowmode (value and unit)``', inline = False)

      embed.add_field(name = 'Ban a member for a limited period of time', value = '``>softban (user) (time and unit)``', inline = False)

      embed.set_footer(text = f"Requested by {ctx.author.name}")
      embed.timestamp = datetime.utcnow()

      await ctx.send(embed=embed)
      
    #mod help command under help group
    @help_command.command(name = 'misc')
    async def misc_help(self, ctx):
      embed = discord.Embed(title = "Moderation commands (Prefix: `>`)", color=ctx.author.color)

      embed.add_field(name = "<command>", value = "``><command> (member) (reason)``", inline = False)

      embed.add_field(name = "<command>", value = "``><command> (member) (reason)``", inline = False)

      embed.add_field(name = "<command>", value = "``<command>(member) (reason)``", inline = False)

      embed.add_field(name = "<command>", value = "``<command> (member) (time + unit)``", inline = False)

      embed.set_footer(text = f"Requested by {ctx.author.name}")
      embed.timestamp = datetime.utcnow()

      await ctx.send(embed=embed)

    #fun help under help group
    @help_command.command(name = 'fun')
    async def fun_help(self, ctx):
      em = discord.Embed(title = 'Fun help menu:', color = ctx.author.color)

      em.add_field(name = 'Get answered in yes or no', value = '``>8ball (message)``', inline = False)

      em.add_field(name = 'Get a funny death for the specified user', value = '``>kill (user)``', inline = False)

      em.set_footer(text = f"Requested by {ctx.author.name}")

      em.timestamp = datetime.utcnow()

      await ctx.send(embed = em)

def setup(bot):
  bot.add_cog(ExampleCog(bot))
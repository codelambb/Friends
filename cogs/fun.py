import discord
from discord import embeds
from discord import client
from discord import message
from discord import user
from discord import errors 
from discord.ext import commands
from discord.ext.commands.core import command 
from discord.ext.commands.errors import BotMissingPermissions, CheckFailure, MissingRequiredArgument
from discord.errors import ClientException, DiscordException
import random 
from random import randint
import time
import asyncio
from asyncio import sleep
from keep_alive import keep_alive
import os
import PIL
import prsaw
from prsaw import RandomStuffV2

from PIL import Image
from io import BytesIO

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

		#on_ready event
    @commands.Cog.listener() # You use commands.Cog.listener() instead of bot.event
    async def on_ready(self):
        print("Fun Cog is Ready!")
		
		#8ball command
    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, msge:str):
      responses=["It is not certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Don't count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Very doubtful."]
      await ctx.send(f':8ball:{random.choice(responses)}')

    #aichat command
    @commands.command()
    async def aichat(self, ctx, *, message):
      if ctx.channel.id == 865106631545454601:
        if ctx.author.id != 862600965940576287:
          rs = RandomStuffV2()
          response = rs.get_ai_response(message)
          await ctx.message.reply(response)

      else:
        await ctx.send(f"I can't chat with you here you have to chat with me in <#865106631545454601>")

    @commands.command()
    async def kill(self, ctx, user : discord.Member =   None):
      if user is not None:
  
        kils = [f"{ctx.author.name} tried to back stab {user.name} but got backstabbed instead ",  
        f"{user.name} fought to the death with {ctx.author.name} and died, couldn't care less.", 
        f"{user.name} couldn't avoid flying with an elytra, failed miserably.", 
        f"{user.name} oofed away.", 
        f"{user.name} wanted to die, so I killed them with my friend Glados!",
        f"{ctx.author.name} passed a bullet right through {user.name}'s empty skull.",
        f"{user.name} was ran over by {ctx.author.name}'s car by 'accident'.",
        f"{user.name} was packed in a coffin and {ctx.author.name} played astronomia, what an honor.",
        f"{ctx.author.name} coded Glados to kill {user.name}. :wave: ",    
        f"{user.name} missed a 5 block mlg, but with a snow block, which they thought was powdered snow.", 
        f"{ctx.author.name} was too lazy to kill {user.name}, instead hired agent 47 for the job. ",
        f"{ctx.author.name} died while trying to hurt {user.name}",   
        ]
        await ctx.send(random.choice(kils))
      else:
        await ctx.send('Aditya was killed by shhoting rpg missile in his buttocks ')     

    @commands.command()
    async def hack(self, ctx, user: discord.Member = None):
      addresses = ["190.187.225.103",
'58.116.116.233',
'232.92.131.5',
'130.58.214.169',
'55.145.252.206',
'122.17.157.250',
'234.154.97.186',
'133.130.22.168',
'61.97.68.240',
'36.26.59.71'
]

      if user is None:
        await ctx.send('Do you want me to hack you empty brain?')
      if user is not None:
        hack = await ctx.send(f'Now hacking **{user.name}**!')
        await asyncio.sleep(3)
        await hack.edit(content = f'**Fetching I.P. address:** {random.choice(addresses)} ')
        await asyncio.sleep(3)
        await hack.edit(content = f"**Logging into Epic Games account now:** {user.name}")
        await asyncio.sleep(3)
        await hack.edit(content =f"Changing password to **{user.name}@gmail.com**")
        await asyncio.sleep(3)
        await hack.edit(content =f"Getting into roblox account using **sim swapping**.")
        await asyncio.sleep(3)
        await hack.edit(content =f"Successfully hacked {user.name}, this is a **very real** hack do not take this lightly.")

    @commands.command()
    async def capturediscord(self,ctx):
      capture=await ctx.send('``Calling Bob and his army to capture discord``')
      await asyncio.sleep(3)
      await capture.edit(content=f'``Bob has made his army ready of ytubers and thanos``')
      await asyncio.sleep(3)
      await capture.edit(content='``Bob charging toward discord private files``')
      await asyncio.sleep(3)
      await capture.edit(content='``Bob is trending on twitter wait a min discord is on twitter lol``')
      await asyncio.sleep(3)
      await capture.edit(content='``Sed bob is flushed out of files by discord dev.``')
      await asyncio.sleep(3)
      await capture.edit(content='``Currently bob is cursing that tweet and thanos for missing his time stone``')

def setup(bot):
  bot.add_cog(ExampleCog(bot))

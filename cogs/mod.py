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
import json

async def get_number_data():
  with open("number.json", "r") as f:
    users = json.load(f)

  return users

async def open_number_data(user):
  users = await get_number_data()

  if str(user.id) in users:
    return

  else:
    users[str(user.id)] = {}
    users[str(user.id)]["number"] = 1

  with open("number.json", "w") as f:
    json.dump(users, f, indent=4)

async def add_number(user):
  users = await get_number_data()
  users[str(user.id)]["number"] += 1

  with open("number.json", "w") as f:
    json.dump(users, f, indent=4)

async def get_warn_data():
  with open("warn.json", "r") as f:
    users = json.load(f)

  return users

async def open_warn_data(user):
  users = await get_warn_data()

  if str(user.id) in users:
    return

  else:
    users[str(user.id)] = {}

  with open("warn.json", "w") as f:
    json.dump(users, f, indent=4)

async def add_warn(user, reason):
  users = await get_warn_data()
  number = await get_number_data()
  n = number[str(user.id)]["number"]
  users[str(user.id)][n] = reason

  with open("warn.json", "w") as f:
    json.dump(users, f, indent=4)

async def remove_warn(user, number):
  users = await get_warn_data()
  del users[str(user.id)][number]

  with open("warn.json", "w") as f:
    json.dump(users, f, indent=4)

async def remove_number(user):
  number = await get_number_data()
  del number[str(user.id)]

  with open("number.json", "w") as f:
    json.dump(number, f, indent=4)  

class ExampleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener() # You use commands.Cog.listener() instead of bot.event
    async def on_ready(self):
        print("Moderation Cog is Ready!")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason="No reason provided"):
      if member == None:
        em=discord.Embed(title='Member object is required')
        await ctx.send(embed=em)

      await open_warn_data(member)
      await open_number_data(member)
      number = await get_number_data()
      users = await get_warn_data()
      await add_warn(member, reason)
      await add_number(member)
      await ctx.send(f"Successfully warned {member.mention} for reason: {reason}")

      if member.bot == True:
        return

      await member.send(f"You have been warned in {ctx.guild.name} by {ctx.author} for reason: {reason}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warns(self, ctx, member: discord.Member = None):
      if member == None:
        em=discord.Embed(title='Member object is required')
        await ctx.send(embed=em)

      await open_warn_data(member)
      users = await get_warn_data()
      em = discord.Embed(title=f"Warns of {member.name}")
      s = 1

      for i in users[str(member.id)]:
        reason = users[str(member.id)][i]
        em.add_field(name=f"{s}) (Warn id: `{i}`)", value=f"`Reason: {reason}`")
        s += 1

      await ctx.send(embed=em)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def remove(self, ctx, member: discord.Member = None, number = None):
      if member == None:
        em=discord.Embed(title='Member object is required')
        await ctx.send(embed=em)

      if number == None:
        em=discord.Embed(title='Id object is required')
        await ctx.send(embed=em)

      await open_warn_data(member)
      users = await get_warn_data()
      await remove_warn(member, str(number))
      await ctx.send(f"Successfully removed {member.mention} warning with id: `{number}`")

      if member.bot == True:
        return

      await ctx.send(f"Your warning in {ctx.guild.name} with id: `{number}` has been removed by {ctx.author}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def clearwarns(self, ctx):
      users = await get_warn_data()
      e = await get_warn_data()
      number = await get_number_data()
      o = await get_number_data()
      for i in users:
        del e[i]

      for x in number:
        del o[x]

      with open("warn.json", "w") as f:
        json.dump(e, f, indent=4)

      with open("number.json", "w") as f:
        json.dump(o, f, indent=4)

      await ctx.send(f"Successfully remove all warning from all the members and reseted the id system!")

    @commands.command(name='kick')#you use @commands.command instead of @bot.command and use ctx, self, (variable for )
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member=None,* , reason=None):
      if member == None:
        em=discord.Embed(title='Member object is required')
        await ctx.send(embed=em)
      else:
        if member == ctx.author:
          em=discord.Embed(title='You are mad or wht.....you cant kick yourself noob')
          await ctx.send(embed=em)
        elif member.top_role>=ctx.author.top_role:
          await ctx.send("You cant kick a user which is equal to you or higher to your rank")
        elif member.bot==True:
          await member.kick(reason=reason)
          embed=discord.Embed(title="Kick", description=f'**Offender:** {member.mention}, {member.id}\n **Reason:** {reason}\n **Responsible mod:** {ctx.author}', color=discord.Color.red())
          await ctx.send(embed=embed)
        else:
          await member.send(f'You have been kicked from ({ctx.guild.name}) for this reason: {reason}')
          await member.kick(reason=reason)
          embed=discord.Embed(title="Kick", description=f'**Offender:** {member.mention}, {member.id}\n **Reason:** {reason}\n **Responsible mod:** {ctx.author}', color=discord.Color.red())
          await ctx.send(embed=embed)
    
    
    @kick.error
    async def kick_error(self,ctx,error):
      if isinstance(error, commands.MissingPermissions):
        em=discord.Embed(title=f'You dont have permission to use this command')
        await ctx.send(embed=em)
      elif isinstance(error, Exception):
        await ctx.send(f'I dont have permissions to use that')  

    @commands.command(name='ban')#you use @commands.command instead of @bot.command and use ctx, self, (variable for )
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member=None,* , reason=None):
      if member == None:
        em=discord.Embed(title='Member object is required')
        await ctx.send(embed=em)
      else:
        if member == ctx.author:
          em=discord.Embed(title='You kick kick yourself!')
          await ctx.send(embed=em)
        elif member.top_role>=ctx.author.top_role:
          await ctx.send("You cannot kick a user which is equal to you or higher to your rank")
        elif member.bot==True:
          await member.ban(reason=reason)
          embed=discord.Embed(title="Kick", description=f'**Offender:** {member.mention}, {member.id}\n **Reason:** {reason}\n **Responsible mod:** {ctx.author}', color=discord.Color.red())
          await ctx.send(embed=embed)
        else:
          await member.send(f'You have been banned from ({ctx.guild.name}) for this reason: {reason}')
          await member.kick(reason=reason)
          embed=discord.Embed(title="ban", description=f'**Offender:** {member.mention}, {member.id}\n **Reason:** {reason}\n **Responsible moderator:** {ctx.author}', color=discord.Color.red())
          await ctx.send(embed=embed)

    @ban.error
    async def ban_error(self,ctx,error):
      if isinstance(error, commands.MissingPermissions):
        em=discord.Embed(title=f'You dont have permission to use this command')
        await ctx.send(embed=em)
      elif isinstance(error, commands.MemberNotFound):
        await ctx.send(f'Member not found')  

    @warn.error
    async def warn_error(self,ctx,error):
      if isinstance(error, commands.MissingPermissions):
        em=discord.Embed(title=f'You dont have permission to use this command')
        await ctx.send(embed=em)
      elif isinstance(error, Exception):
        await ctx.send(f'I dont have permissions to use that')  


    @warns.error
    async def warns_error(self,ctx,error):
      if isinstance(error, commands.MissingPermissions):
        em=discord.Embed(title=f'You dont have permission to use this command')
        await ctx.send(embed=em)
      elif isinstance(error, commands.MemberNotFound):
        await ctx.send(f'Member not found')  

    @remove.error
    async def remove_error(self,ctx,error):
      if isinstance(error, commands.MissingPermissions):
        em=discord.Embed(title=f'You dont have permission to use this command')
        await ctx.send(embed=em)
      elif isinstance(error, commands.MemberNotFound):
        await ctx.send(f'Member not found')
      else:
        await ctx.send(f"No matching id for that user's warnings")  

    @clearwarns.error
    async def clearwarns_error(self,ctx,error):
      if isinstance(error, commands.MissingPermissions):
        em=discord.Embed(title=f'You dont have permission to use this command')
        await ctx.send(embed=em)

    #lock command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.message.channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions = False)
        em = discord.Embed(title=f"Successfully done!\n\n", description=f":lock: I have successfully locked <#{channel.id}> for the server's default role!", color=discord.Color.green())
        await ctx.send(embed=em)

    #unlock command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.message.channel

        await channel.set_permissions(ctx.guild.default_role, send_messages=True, add_reactions = True)
        em = discord.Embed(title=f"Successfully done!\n\n", description=f":lock: I have successfully unlocked <#{channel.id}> for the server's default role!", color=discord.Color.green())
        await ctx.send(embed=em)
    
    #mute command
    @commands.command()
    @commands.has_permissions(manage_roles = True)
    async def mute(self, ctx, member: discord.Member, time):
      id = 859768827482472449
      time_amount = int(time[:-1])
      time_unit = (time[-1])
      if time_unit == "s":
        seconds = time_amount
        role = get(ctx.guild.roles, id=id)
        await member.add_roles(role)
        await ctx.send(f'The user {member.name} has been muted for {time}')
        await asyncio.sleep(seconds)
        await member.remove_roles(role)
        await ctx.send(f'The user {member.name} has been unmuted.')


      elif time_unit == "m":
        seconds = time_amount * 60
        role = get(ctx.guild.roles, id=id)
        await member.add_roles(role)
        await ctx.send(f'The user {member.name} has been muted for {time}')
        await asyncio.sleep(seconds)
        await member.remove_roles(role)
        await ctx.send(f'The user {member.name} has been unmuted.')


      elif time_unit == "h":
        seconds = time_amount * 60 * 60
        role = get(ctx.guild.roles, id=id)
        await member.add_roles(role)
        await ctx.send(f'The user {member.name} has been muted for {time}')
        await asyncio.sleep(seconds)
        await member.remove_roles(role)
        await ctx.send(f'The user {member.name} has been unmuted.')
    
    @mute.error
    async def mute_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send(':no: You lack the permissions to perform that action!')

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def forceunmute(self,ctx,member: discord.Member):
        id = 859768827482472449
        role = get(ctx.guild.roles, id=id)
        await member.remove_roles(role)
        await ctx.send(f'The user {member.name} has been unmuted.')

    #softban command
    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def softban(self, ctx, member : discord.Member, time,*, reason):
      time_amount = int(time[:-1])
      time_unit = (time[-1])
      embed = discord.Embed(title = f"You have been banned from the guild{ctx.guild.name} ")
      if time_unit == "s":
        seconds = time_amount
        embed.add_field(name = "Ban time:", value = f"{time}", inline = True)
        embed.add_field(name = "Reason:", value = f"{reason}", inline = True)
        await member.ban(reason = reason)
        await member.send(embed = embed)
        await asyncio.sleep(seconds)
        member.unban

      elif time_unit == "m":
        seconds = time_amount * 60
        embed.add_field(name = "Ban time:", value = f"{time}", inline = True)
        embed.add_field(name = "Reason:", value = f"{reason}", inline = True)
        await member.ban(reason = reason)
        await member.send(embed = embed)
        await asyncio.sleep(seconds)
        member.unban

      elif time_unit == "h":
        seconds = time_amount * 60 * 60
        embed.add_field(name = "Ban time:", value = f"{time}", inline = True)
        embed.add_field(name = "Reason:", value = f"{reason}", inline = True)
        await member.ban(reason = reason)
        await member.send(embed = embed)
        await asyncio.sleep(seconds)
        member.unban

    @softban.error
    async def softban_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to use that command.")
        raise error

    #slowmode command
    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, time = None):
        if time == None:
            em = discord.Embed(title="<a:no:801303064178196520> Please provide the time next time!", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if time[-1] != 's' and time[-1] != 'm' and time[-1] != 'h':
            em = discord.Embed(title="<a:no:801303064178196520> You need to have your last digit for time as `s/m/h` for example 5h", color=discord.Color.red())
            await ctx.send(embed=em)
            return

        if time[-1] == 's':
            y = int(time[:-1])
            if y > 21600:
                em = discord.Embed(title="<a:no:801303064178196520> The limit of the slowmode is till 6 hours only!", color=discord.Color.red())
                await ctx.send(embed=em)
                return     

            await ctx.channel.edit(slowmode_delay=y)
            await ctx.send(f"Set the slowmode delay in this channel to {time} seconds!")

        elif time[-1] == 'm':
            x = int(time[:-1]) * 60
            if x > 21600:
                em = discord.Embed(title="<a:no:801303064178196520> The limit of the slowmode is till 6 hours only!", color=discord.Color.red())
                await ctx.send(embed=em)
                return  

            await ctx.channel.edit(slowmode_delay=x)
            await ctx.send(f"Set the slowmode delay in this channel to {time} seconds!")

        elif time[-1] == 'h':
            j = int(time[:-1]) * 3600
            if j > 21600:
                em = discord.Embed(title="<a:no:801303064178196520> The limit of the slowmode is till 6 hours only!", color=discord.Color.red())
                await ctx.send(embed=em)
                return  

            await ctx.channel.edit(slowmode_delay=j)
            await ctx.send(f"Set the slowmode delay in this channel to {time} seconds!")


    @slowmode.error
    async def slowmode_error(self,ctx,error):
      if isinstance(error,commands.MissingPermissions):
        await ctx.send("You don't have the permissions to use this command.")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def reminder(self, ctx, *, warn =  None):
      id = 865106631355531332
      channe = get(ctx.guild.channels, id=id)
      if warn is not None:
        await ctx.message.delete()
        meat = await ctx.send("Mention the user you want to remind.`.")
        try:
            yoo = await self.bot.wait_for(
                "message",
                timeout = 30,
                check = lambda message: message.author == ctx.author
                               and message.channel == ctx.channel
                  
                )
            em = discord.Embed(title = f'Non-Warn reminder!', color = ctx.author.color)
            em.add_field(name = f"reminder:", value = warn, inline = False)
            em.add_field(name = "Resonsible moderator:", value = ctx.author.name, inline = False )
            em.add_field(name = f"Offendor:", value = yoo.content, inline = False)
            em.set_thumbnail(url = "http://www.isharad.com/wp-content/uploads/2014/12/IMG_1782.gif")
            await channe.send(embed = em)
            await meat.delete()
            await yoo.delete()
        except asyncio.TimeoutError:
          await ctx.send("Sorry, you didn't reply in time!")

    @commands.Cog.listener()
    async def on_member_join(self, ctx, user: discord.Member):
      user = self.bot.fetch_user(user.id)
      boom = 859364313626312705
      channe = get(ctx.guild.channels, id=boom)
      await channe.send(f"{user} has joined the server, we are at {ctx.guild.member_count} members!")

    @commands.Cog.listener()
    async def on_member_leave(self, ctx, user: discord.Member):
      user = self.bot.fetch_user(user.id)
      id = 859364313626312705
      channe = get(ctx.guild.channels, id=id)
      await channe.send(f"{user} has left the server we are down to {ctx.guild.member_count} members.")

            

    @reminder.error
    async def reminder_error(self, ctx, error):
      if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have the permission to use that command!")




def setup(bot):
  bot.add_cog(ExampleCog(bot))
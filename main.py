import discord
intents = discord.Intents.all()

from discord.ext import commands
client = commands.Bot(command_prefix=';', case_insensitive=True, intents=intents)

import nacl

import asyncio
import time
from time import sleep
import random
import os

def Find(str, pattern):
  for x in range(len(str)):
    patternFound = True
    for y in range(len(pattern)):
      if (x + y > len(str) - 1):
        patternFound = False
        break
      if (str[x + y] != pattern[y]):
        patternFound = False
        break
    if patternFound:
      return True
    else:
      continue
  return False

@client.event
async def on_ready():
  print("Bot is ready.")

mutes = []
jailed = []

@client.event
async def on_message(message):
  if message.author.bot:
    return
  
  for mutedRecord in mutes:
    if (mutedRecord['id'] == message.author.id):
      if (time.time() - mutedRecord['start'] >= mutedRecord['length']):
        mutes.remove(mutedRecord)
      else:
        await message.delete()
        return

  if Find(message.content, "https://") or Find(message.content, ".com"):
    await message.delete()
    await message.channel.send(f'🚫 Links are not allowed {message.author.mention}!')
  await client.process_commands(message)

@client.event
async def on_member_join(member):
  # Join Message
  channel = client.get_channel(915601167512375356)
  pfp = member.avatar_url
  await channel.send("😀 Welcome to the Server {}!\n{}".format(member.mention, pfp))

@client.event
async def on_member_remove(member):
  # Leave Message
  channel = client.get_channel(915659741718540360)
  pfp = member.avatar_url
  await channel.send("😔 {} just left the server.\n{}".format(member.mention, pfp))

# Normal

@client.command()
async def kick(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Admin")
  if role in ctx.message.author.roles:
    await member.kick()
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Admin role to use this command')

@client.command()
async def ban(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Admin")
  if role in ctx.message.author.roles:
    await member.ban()
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Admin role to use this command')

@client.command()
async def rename(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Admin")
  if role in ctx.message.author.roles:
    name = ctx.message.content[(len(';rename') + len(member.mention) + 1):len(ctx.message.content)]
    await member.edit(nick=name)
    oldName = member.name
    await ctx.send("✅ Successfully renamed {} from {} to '{}'".format(member.mention, oldName, name))
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Admin role to use this command')

@client.command()
async def clear(ctx, amount=10):
  role = discord.utils.get(ctx.guild.roles, name="Commands")
  if role in ctx.message.author.roles:
    await ctx.channel.purge(limit=amount)
    await ctx.send("✅ Successfully deleted {} messages! [THIS MESSAGE WILL BE DELETED AUTOMATICALLY]".format(amount), delete_after=1.5)

@client.command()
async def pfp(ctx, member: discord.Member):
  await ctx.send(member.avatar_url)

@client.command()
async def ss(ctx, n: int or float):
  suffixes = ["K", "M", "B", "T", "Qd", "Qu"];
  for index, suffix in enumerate(suffixes):
    if (n >= pow(1000, index + 1)) and (n < pow(1000, index + 2)):
      if int(n/pow(1000, index + 1)) == n/pow(1000, index + 1):
        # The calculated result is an integer
        await ctx.send("✅ " + str(int(n/pow(1000, index + 1))) + suffix)
        return;
      else:
        # The calculated result is a float
        await ctx.send("✅ " + str(n/pow(1000, index + 1)) + suffix)
        return;
  await ctx.send("✅ " + n)

@client.command()
async def sc(ctx, n: int):
  strNumber = str(n)[::-1]
  formattedNumber = ''
  iterations = 0;
  for i in range(len(strNumber)):
    formattedNumber += strNumber[i]
    if (i == len(strNumber) - 1): break
    iterations += 1
    if (iterations == 3):
      iterations = 0
      formattedNumber += ','
  await ctx.send("✅ " + formattedNumber[::-1])

@client.command()
async def mute(ctx, member: discord.Member, units: int, timeScale: str):
  role = discord.utils.get(ctx.guild.roles, name="Admin")
  if role in ctx.message.author.roles:
    if (ctx.author == member): return
    length = units;
    if (timeScale == 'secs'):
      length *= 1
    elif (timeScale == 'mins'):
      length *= 60    
    elif (timeScale == 'hrs'):
      length *= 60
      length *= 60
    elif (timeScale == 'days'):
      length *= 60
      length *= 60
      length *= 24
    else:
      await ctx.send("🚫 I don't know what units are ''" + timeScale + "''.   Try secs, mins, hrs or days.")
      return
    mutes.append({'id':  member.id,'length': length, 'start': time.time()})
    await ctx.send("✅ Successfully muted " + member.mention + " for " + str(units) + " " + timeScale)
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Admin role to use this command')

@client.command()
async def unmute(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Admin")
  if role in ctx.message.author.roles:
    if (ctx.author == member): return
    role = discord.utils.get(ctx.guild.roles, name="Admin")
    if role in member.roles:
      for muteRecord in mutes:
        if (muteRecord['id'] == member.id):
          mutes.remove(muteRecord)
          await ctx.send("✅ " + member.mention + " has been unmuted.")
          return
      await ctx.send("🚫 " + member.mention + " is not muted.")
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Admin role to use this command')

@client.command()
async def onmobile(ctx, member: discord.Member):
  await ctx.send("✅ " + member.name + " is " + ('on' if member.is_on_mobile() else 'not on') + ' mobile.')

cmdsTexts = [
  "\n**None:**",
  ';pfp (mention) - The bot will send the profile picture of the mentioned user',
  ';ss (number) - Abberivatves a number with suffixes',
  ';sc (number) - Simplifies  a number with commas',
  ';onmobile (mention) - The bot will tell whether the mentioned user is on mobile or not',
  ';scatter (message) - The bot will send a scattered form of the message',
  ";recall (mention) - Recalls the mentioned user's last message scattered, not to be used offensively",
  ';ping - The bot will respond with "pong"',
  ';memberscnt - The bot will respond with the current member count of the server',
  ";banner - The bot will send the banner of the current server",
  "\n**Commands:**",
  ";hasrole (mention) (roleName) - The bot will respond with wether the user has a role with the roleName.",
  ';call (mention) - Tells the mentioned user to come',
  ';clear (depth) - Clears the current text channel with respect to depth',
  ";join - The bot will join the message author's voice channel, if the message author is in one",
  ";leave - The bot will leave it's current voice channel, if it's in one",
  ";joinedat (mention) - The bot will respond with the date the mentioned user joined the server at.",
  ';repeat (repetitions) (message) - The bot will send some messages with respect to repetitions and message',
  "\n**Admin:**",
  ";kick (mention) - The mentioned member will be kicked from the server",
  ";ban (mention) - The mentioned user will be banned from the server",
  ';mute (mention) (magnitude) (units) - Mutes a member from sending messages. Units: secs | mins | hrs | days',
  ';unmute (mention) - Unmutes a member that is currently muted',
  ';rename (mention) (new name) - Renames the mentioned user to the new name',
  ';giverole (mention) (roleName) - Gives the mention member the named role',
  ";removerole (mention) (roleName) - Removes the role from the mentioned member",
  "\n**Police:**",
  ";jail (mention) - Jails the mentioned user",
  ";unjail (mention) - Unjails the mentioned user",
]

@client.command()
async def cmds(ctx):
  message = '✅ Here are all of the commands, with the required roles:'
  for commandText in cmdsTexts:
    message += "\n"
    message += commandText
  message += '\nExpect more commands be added in the future!'
  await ctx.send(message)

@client.command()
async def repeat(ctx, number: int):
  role = discord.utils.get(ctx.guild.roles, name="Commands")
  if role in ctx.message.author.roles:
    for i in range(number):
      await ctx.send(ctx.message.content[(len(';repeat ') + len(" " + str(number))):len(ctx.message.content)])

def scatterMessage(message):
  newMessage = "*"
  for i in range(len(message)):
    newMessage += message[i].upper() if (random.randint(1, 2) == 1) else message[i].lower()
  newMessage += "*"
  return newMessage

@client.command()
async def scatter(ctx):
  message = ctx.message.content[len(';scatter '):len(ctx.message.content)]
  await ctx.send("✅ " + scatterMessage(message))

@client.command()
async def recall(ctx, member: discord.Member):
  async for message in ctx.channel.history(limit=200):
      if (message.author == member):
          await ctx.send(scatterMessage(message.content))
          return

@client.command()
async def ping(ctx):
  await ctx.send("pong")

@client.command()
async def call(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Commands")
  if role in ctx.message.author.roles:
    await ctx.send(member.mention + " come! :pray:")

@client.command()
async def memberscnt(ctx):
  await ctx.send(f'✅ This server has {ctx.guild.member_count} {"member" if ctx.guild.member_count <= 1 else "members."}')

@client.command()
async def banner(ctx):
  if ctx.guild.banner:
    await ctx.send("✅\n" + ctx.guild.banner)
  else:
    await ctx.send("🚫 This server does not have a banner.")

@client.command()
async def giverole(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Admin")
  if role in ctx.message.author.roles:
    roleName = ctx.message.content[(len(';giverole ') + len(member.mention) + 1):len(ctx.message.content)]
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    if role:
      await member.add_roles(role)
      await ctx.send(f'✅ Successfully added "{roleName}" role to {member.mention}!')
    else:
      await ctx.send(f'🚫 Role "{roleName}" has not been found.')
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Admin role to use this command')

@client.command()
async def removerole(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Admin")
  if role in ctx.message.author.roles:
    roleName = ctx.message.content[(len(';removerole') + len(member.mention) + 1 + 1):len(ctx.message.content)]
    role = discord.utils.get(ctx.guild.roles, name=roleName)
    if role:
      await member.remove_roles(role)
      await ctx.send(f'✅ Successfully removed "{roleName}" from {member.mention}!')
    else:
      await ctx.send(f'🚫 Role "{roleName}" has not been found.')
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Admin role to use this command')
  
    

@client.command()
async def hasrole(ctx, member: discord.Member):
  roleName = ctx.message.content[(len(";hasrole") + len(member.mention) + 1 + 1):len(ctx.message.content)]
  role = discord.utils.get(ctx.guild.roles, name=roleName)
  if role in ctx.message.author.roles:
    await ctx.send(f'✅ {member.mention} has the "{roleName}" role.')
  else:
    await ctx.send(f'🚫 {member.mention} does not have the "{roleName}" role.')
    
@client.command()
async def join(ctx):
  role = discord.utils.get(ctx.guild.roles, name="Commands")
  if role in ctx.message.author.roles:
    if (ctx.author.voice != None):
      await ctx.author.voice.channel.connect()
    else:
      await ctx.send("🚫 You are not in a voice channel!")
  
@client.command()
async def leave(ctx):
  role = discord.utils.get(ctx.guild.roles, name="Commands")
  if role in ctx.message.author.roles:
    await ctx.guild.voice_client.disconnect()

@client.command()
async def joinedat(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Commands")
  if role in ctx.message.author.roles:
    await ctx.send(f'✅ {member.mention} joined the server at {member.joined_at}.')

jailChannelId = 984859983801876500

@client.command()
async def jail(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Police")
  if role in ctx.message.author.roles:
    if (member.voice != None):
      jailedRecord = {'member': member}
      jailChannel = client.get_channel(jailChannelId)
      jailed.append(jailedRecord)
      await member.move_to(jailChannel)
      await ctx.send("✅ Successfully jailed " + member.mention + "!")
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Police role to use this command')

@client.command()
async def unjail(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name="Police")
  if role in ctx.message.author.roles:
    for jailedRecord in jailed:
      if (jailedRecord['member'] == member):
        jailed.remove(jailedRecord)
        await ctx.send("✅ " + member.mention + " has been unjailed.")
  else:
    await ctx.send(f'🚫 {ctx.author.mention} You do not have the Police role to use this command')

@client.event
async def on_voice_state_update(member, before, after):
  if (after.channel.id != jailChannelId):
    for jailedRecord in jailed:
      if (jailedRecord['member'] == member):
        jailChannel = client.get_channel(jailChannelId)
        await member.move_to(jailChannel)

client.run(os.environ['token'])

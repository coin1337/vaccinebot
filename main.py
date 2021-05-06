import discord
from discord.ext import commands
import os
from keep_alive import keep_alive
import vbcommands

client = commands.Bot(command_prefix='>')

@client.event
async def on_ready():
  print('Logged in as {0.user}'.format(client))
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='for Vaccines (>)'))

@client.event   
async def on_message(message):
  if message.author == client.user:
    return

  await client.process_commands(message)

@client.command()
async def data(ctx, *, arg):
  await ctx.send(embed = vbcommands.data(arg.title()))

@client.command()
async def find(ctx, *, arg):
  await ctx.send(embed = vbcommands.find(arg))

@client.command()
async def vaccinate(ctx, member: discord.Member):
  await ctx.send(embed = vbcommands.vaccinate(ctx, member))
  if ctx.message.author.guild_permissions.administrator:
    await member.add_roles(discord.utils.get(ctx.guild.roles, name='Vaccinated'))

@client.command()
async def links(ctx):
  await ctx.send(embed = vbcommands.links())

@client.command()
async def info(ctx, arg):
  await ctx.send(embed = vbcommands.info(arg))
  
@client.command()
async def vbhelp(ctx):
  await ctx.send(embed = vbcommands.bot_help())

keep_alive()
client.run(os.getenv('TOKEN'))

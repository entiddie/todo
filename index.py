import discord
from discord.ext import commands
import os


client = commands.Bot(
    command_prefix=commands.when_mentioned_or("todo "),
    case_insensitive=True,
)

client.remove_command('help')


# Loading Cogs


@client.command()
async def load(ctx, extension):
	client.load_extension(f"cogs.{extension}")


@client.command()
async def unload(ctx, extension):
	client.unload_extension(f"cogs.{extension}")


for filename in os.listdir('./cogs'):
	if filename.endswith('.py'):
		client.load_extension(f"cogs.{filename[:-3]}")



# Events


@client.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(client.user))


# Basic Commands


@client.command()
async def ping(ctx):
    e = discord.Embed(
        color=0x2f3136, description='<:check:779967322118946846> Bot servers online'
    )
    
    await ctx.send(embed=e)


client.run('')

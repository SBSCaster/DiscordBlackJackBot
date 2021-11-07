import discord
from discord.ext import commands
import casino_bot

cogs = [casino_bot]

client = commands.Bot(command_prefix='$', intents=discord.Intents.all())

for index in range(len(cogs)):
  cogs[index].setup(client)

client.run('OTA2NDg2OTMwNjAxMDI5NjUz.YYZVvQ.Rsdo0vuF_2O2WNhzyskePgG2q4U')


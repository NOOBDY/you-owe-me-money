from os import environ

from discord.ext import commands
from discord.ext.commands import Context
from discord import Message
import discord

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.event
async def on_message(message: Message):
    print(message.content)
    await bot.process_commands(message)


@bot.command()
async def test(ctx: Context):
    await ctx.send("fuck you")

bot.run(environ["TOKEN"])

'''
discord bot for almost all the functions
'''

import datetime
import asyncio
from textwrap import dedent
from os import environ

from discord.ext import commands
from discord.ext.commands import Context
from discord import Message
import discord

import command
from db.record import Record
from test.mock_utils import reset, add_record, delete_record, list_records, find_record

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)


@bot.command()
async def cli(ctx: Context):
    if len(ctx.message.mentions) == 1:
        member_id = (ctx.message.mentions[0]).id
        print(member_id)
    else:
        print("you fail")

bot.run(environ["DISCORD_BOT_TOKEN"])

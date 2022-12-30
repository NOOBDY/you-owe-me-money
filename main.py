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
async def add(ctx: Context):
    '''
    to make a new record
    '''
    command: list = (str(ctx.message.content)).split()
    if len(command) < 4:
        await ctx.send("there are some information missing, please type the instruction again.")
        return

    # check if the second is userID
    if len(ctx.message.mentions) == 1:
        member_id = (ctx.message.mentions[0]).id
    else:
        await ctx.send("please tag only the user to store the information of debtor")
        return

    if not command[2].isdigit():
        print(type(command[2]))
        await ctx.send("the amount of money is invalid")
        return

    new_record: Record = Record(
        ctx.message.author.id, member_id, int(command[2]), command[3])

    toClient: str = "%s $%i %s %s borrowed from %s" % (str(datetime.date.today()), new_record.get_amount(
    ), new_record.get_title(), ("<@"+str(new_record.get_debtor_id())+">"), ("<@"+str(new_record.get_creditor_id())+">"))

    add_record(new_record)
    print(list_records())

    a = list(list_records().values())
    for i in range(len(a)):
        print(a[i].get_creditor_id(), a[i].get_debtor_id(),
              a[i].get_amount(), a[i].get_title())

    await ctx.send(toClient)
    return


@bot.command()
async def to_me(ctx: Context):
    '''
    who borrowed money from me
    '''
    ...


@bot.command()
async def to_others(ctx: Context):
    '''
    I borrowed money form whom
    '''
    ...


@bot.command()
async def modify(ctx: Context):
    '''
    can modify name, amount of money, or item info
    '''

    # [1]=record ID,[2]= name/amount/info,[3]= value
    command: list = (str(ctx.message.content)).split()
    if len(command) != 4:
        await ctx.send("there are some information missing, please type the instruction again")
        return

    record: Record = find_record(int(command[1]))

    whatever = command[3]  # store name or amount or info
    if (command[2] == "name"):
        if len(ctx.message.mentions) == 1:
            member_id = (ctx.message.mentions[0]).id
        else:
            await ctx.send("please tag only the user to store the information of debtor")
            return
        record.set_debtor_id(member_id)

    elif (command[2] == "amount"):
        if not whatever.isdigit():
            await ctx.send("the amount of money is invalid")
            return
        else:
            whatever = int(whatever)
        record.set_amount(whatever)

    elif (command[2] == "info"):
        record.set_title(whatever)

    else:
        await ctx.send("we don't know what you want to modify")
        return

    toClient: str = "modified:\n%s $%i %s %s borrowed from %s" % (str(datetime.date.today()), record.get_amount(
    ), record.get_title(), ("<@"+str(record.get_debtor_id())+">"), ("<@"+str(record.get_creditor_id())+">"))

    await ctx.send(toClient)

    print(list_records())
    a = list(list_records().values())
    for i in range(len(a)):
        print(a[i].get_creditor_id(), a[i].get_debtor_id(),
              a[i].get_amount(), a[i].get_title())

    return


@bot.command()
async def remove(ctx: Context):
    '''
    to remove a certain record
    '''

    command: list = (str(ctx.message.content)).split()
    if len(command) != 2:
        await ctx.send("there are some information missing, please type the instruction again?")
        return

    delete_record(int(command[1]))

    await ctx.send("delete successfully")


@bot.command()
async def clear(ctx: Context):
    '''
    to clear a certain record
    '''

    command: list = (str(ctx.message.content)).split()
    if len(command) != 2:
        await ctx.send("there are some information missing, please type the instruction again...")
        return

    record: Record = find_record(int(command[1]))
    record.clear()

    await ctx.send("clear successfully")


@bot.command()
async def how(ctx: Context):
    '''
    let user knows how to use these instructions
    '''
    total = dedent("""
    ```yaml
    $new
    ```
    for register to a new user, just type it

    ```yaml
    $record {@user} {Money} {item}
    ```
    for appending a new record of you lent other people money,type with the format up above
    for example, $record @you-owe-me-money 100 dinner

    ```yaml
    $check
    ```
    for checking the total amount money of each person who had borrowed from you, just type it

    ```yaml
    $modify {-flag} {@user} {Money} {item}
    ```
    you can modify your record by typing this, the flag can be

    -m, which means you want to change the amount of money

    -n, which means you want to change the debtor's name

    -i, which means you want to change to info of the item


    and the last three must be the same to the record that you want to modify,
    otherwise it can't find the record, nothing will be modified

    next, the robot will ask you to type the correct information so that
    the record will be the correct one

    ```yaml
    $remove {@user} {Money} {item}
    ```
    for removing a certain record, just type the record the the last three information correctly, otherwise the robot can't
    find the record, there is no record will be removed
    you can use $check you check whether it is removed or not
    """)

    await ctx.send(total)

bot.run(environ["DISCORD_BOT_TOKEN"])

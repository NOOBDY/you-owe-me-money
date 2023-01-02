'''
discord bot for almost all the functions
'''

from textwrap import dedent
from os import environ

from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context

from db import (
    Record,
    add_record,
    delete_record,
    find_record,
    creditor_records,
    debtor_records,
    update_record,
)

intents = Intents.default()
intents.message_content = True

PREFIX = "$"

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=intents,
    help_command=None
)


@bot.command()
async def add(ctx: Context):
    '''
    to make a new record
    '''
    msg = ctx.message

    command: list = (str(msg.content)).split()
    if len(command) < 4:
        await ctx.send("there are some information missing, please type the instruction again.")
        return

    # check if the second is userID
    if len(msg.mentions) < 1 or len(msg.mentions) > 2:
        await ctx.send("wrong user mention")
        return

    if len(msg.mentions) == 2 and msg.mentions[0].id != msg.author.id:
        await ctx.send("only the creditor or the debtor can create records")
        return

    if not command[len(msg.mentions) + 1].isdigit():
        await ctx.send("the amount of money is invalid")
        return

    debtor_id = msg.mentions[0].id
    creditor_id = msg.author.id if len(msg.mentions) == 1 else msg.mentions[1].id

    record: Record = Record(
        creditor_id,
        debtor_id,
        int(command[len(msg.mentions) + 1]),
        " ".join(command[len(msg.mentions) + 2:])
    )

    add_record(record)

    await ctx.send(record.to_discord_message())


@bot.command()
async def own(ctx: Context):
    '''
    who borrowed money from me
    '''

    author_id = ctx.message.author.id

    records = creditor_records(author_id)

    if len(records) == 0:
        await ctx.send("no records found")

    for record in records:
        await ctx.send(f"#{record.get_record_id()} {record.to_discord_message()}")


@bot.command()
async def owe(ctx: Context):
    '''
    I borrowed money form whom
    '''

    author_id = ctx.message.author.id

    records = debtor_records(author_id)

    if len(records) == 0:
        await ctx.send("no records found")

    for record in records:
        await ctx.send(f"#{record.get_record_id()} {record.to_discord_message()}")


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

    record = find_record(int(command[1]))

    if not record:
        await ctx.send("no record found with the given ID")
        return

    arg = command[3]  # store name or amount or info

    if command[2] == "name":
        if len(ctx.message.mentions) == 1:
            member_id = (ctx.message.mentions[0]).id
        else:
            await ctx.send("please tag only the user to store the information of debtor")
            return
        record.set_debtor_id(member_id)

    elif command[2] == "amount":
        if not arg.isdigit():
            await ctx.send("the amount of money is invalid")
            return

        record.set_amount(int(arg))

    elif command[2] == "title":
        record.set_title(arg)

    else:
        await ctx.send("we don't know what you want to modify")
        return

    await ctx.send(record.to_discord_message())

    return


@bot.command()
async def remove(ctx: Context):
    '''
    to remove a certain record
    '''

    command: list = (str(ctx.message.content)).split()
    if len(command) != 2:
        await ctx.send("there are some information missing, please type the instruction again")
        return

    record = find_record(int(command[1]))

    if not record:
        await ctx.send("no record found with the given ID")
        return

    if record.get_creditor_id() != ctx.message.author.id:
        await ctx.send("only the creditor can remove debts")
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
        await ctx.send("there are some information missing, please type the instruction again")
        return

    record = find_record(int(command[1]))

    if not record:
        await ctx.send("no record found with the given ID")
        return

    if record.get_creditor_id() != ctx.message.author.id:
        await ctx.send("only the creditor can clear debts")
        return

    record.clear()

    update_record(record)

    await ctx.send("clear successfully")


@bot.command(aliases=["help"])
async def usage(ctx: Context):
    '''
    let user knows how to use these instructions
    '''

    total = dedent(f"""
    command prefix: `{PREFIX}`
    required field: `<>`
    optional field: `[]`

    `add <debtor> [creditor] <amount> <title>`

    `own`

    `owe`

    `modify <record-id> <debtor|amount|title> <value>`

    `clear <record-id>`

    `remove <record-id>`
    """)

    await ctx.send(total)

if __name__ == "__main__":
    bot.run(environ["DISCORD_BOT_TOKEN"])

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


class Record:
    '''
    to store the information of one record
    '''

    def __init__(self, name: str = "", debtor: str = "", date: str = "",
                 amount: int = 0, info: str = ""):
        self.name = name               # username
        self.debtor: str = debtor      # debtor who borrow money from you
        self.date: str = date          # the date that event happened
        self.amount: int = amount      # how much you lent him or her
        self.info: str = info          # the info of the item

    def print_record(self):
        '''
        print one record
        '''
        print(self.date+"  $"+str(self.amount)+"  "+self.info +
              "  "+self.debtor+" borrowed from "+self.name)


class User:
    '''
    to store the data of each user
    '''

    def __init__(self, name: str = "", user_id: str = ""):
        self.name = name                      # username
        self.user_id = user_id                  # user ID in discord
        # for all the debtors and the total money of each
        self.debtors: dict[str, int] = dict()
        self.records: list[Record] = list()           # store all the records

    def append_record(self, record: Record):
        '''
        append record to the list:records and calculate the total amount of money of each
        '''
        if record.debtor in self.debtors:
            self.debtors[record.debtor] += record.amount
        else:
            self.debtors[record.debtor] = record.amount

        self.records.append(record)

    def modify_record(self, current_name: str, new_name: str, current_amount: int, new_amount: int):
        '''
        to modify the value of dict:debtors
        '''
        # modify name, total of each person will change as well
        if current_name != new_name:
            # remove the wrong person's amount
            self.debtors[current_name] -= current_amount

            # append the amount to the correct person
            if new_name not in self.debtors:
                self.debtors[new_name] = current_amount
            else:
                self.debtors[new_name] += current_amount

        # modify amount, in the same person
        if current_amount != new_amount:
            self.debtors[current_name] += (new_amount-current_amount)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
all_users: list[User] = list()  # store all the Users


def save_record(record: Record, all_users: list) -> None:
    '''
    append a record for a certain user
    '''
    for i, user in enumerate(all_users):
        if user.name == record.name:
            all_users[i].append_record(record)
            return record.date + "  $" + str(record.amount)+"  "+record.info+"  "+record.debtor+" borrowed from "+all_users[i].user_id


def search(debtor: str, amount: int, info: str, thing: str, myself: User):
    '''
    to search for the certain record we are finding
    '''
    for i, user in enumerate(myself.records):
        if user.debtor == debtor and user.amount == amount and user.info == info:
            if thing == "-n":
                return "please type new name for modifying", i
            if thing == "-m":
                return "please type new amount of money for modifying", i
            if thing == "-i":
                return "please type new info for modifying", i
            break

    return "have no data that you mentioned", -99


def replace(index: int, thing: str, new_thing, myself: User):
    '''
    to change to wrong value to the correct value
    '''
    current_name = myself.records[index].debtor
    current_amount = myself.records[index].amount
    if thing == "-n":
        # modify $check
        new_name = new_thing
        new_amount = myself.records[index].amount
        myself.modify_record(current_name, new_name,
                             current_amount, new_amount)
        myself.records[index].debtor = str(new_thing)

    elif thing == "-m":
        # modify $check
        new_name = myself.records[index].debtor
        new_amount = new_thing
        myself.modify_record(current_name, new_name,
                             current_amount, new_amount)
        myself.records[index].amount = int(new_thing)

    elif thing == "-i":
        myself.records[index].info = str(new_thing)

    return myself.records[index].date+"  $"+str(myself.records[index].amount)+"  "+myself.records[index].info+"  "+myself.records[index].debtor+" borrowed from "+myself.user_id


def find_myself(name: str):
    '''
    find the user in the whole user list
    '''
    myself: User = User()

    for _, user in enumerate(all_users):
        if user.name == name:
            myself = user
            return myself

    return myself


@bot.command()
async def new(ctx: Context):
    '''
    to create a new account for user
    '''
    # if account is already exist
    myself = find_myself(str(ctx.author))
    if myself.name != "":
        await ctx.send("the account is already exist")
        return

    new_user: User = User(str(ctx.author), "<@"+str(ctx.author.id)+">")
    all_users.append(new_user)

    message: str = new_user.user_id + \
        " is the new user, the whole name is "+new_user.name
    await ctx.send(message)


@bot.command()
async def record(ctx: Context):
    '''
    to make a new record
    '''
    # if the user has no account
    myself = find_myself(str(ctx.author))
    if myself.name == "":
        await ctx.send("there is no user data of you."
                       "if you want to register, please type`$new`")
        return

    # command[1] = userID, command[2]=amount of money, command[3]= info
    command: list = (str(ctx.message.content)).split()
    if len(command) != 4:
        await ctx.send("there are some information missing, please type the instruction again")
        return

    # check if the second is userID
    if not (str(command[1])[:2] == "<@" and str(command[1][-1]) == ">"):
        await ctx.send("please tag the user to store the information of debtor")
        return

    if not command[2].isdigit():
        print(type(command[2]))
        await ctx.send("the amount of money is invalid")
        return

    # if all fine
    new_record: Record = Record(str(ctx.author), command[1], str(
        datetime.date.today()), int(command[2]), str(command[3]))
    await ctx.send(save_record(new_record, all_users))


@bot.command()
async def check(ctx: Context):
    '''
    to check to total amount of money of each debtors
    '''
    # if there is no user
    myself = find_myself(str(ctx.author))
    if myself.name == "":
        await ctx.send("there is no user data of you."
                       "if you want to register, please type`$new`")
        return

    # if have no debtors
    if len(myself.debtors) == 0:
        await ctx.send("there is no debtors")
        return

    # if all fine
    for debtor, amount in myself.debtors.items():
        each_record: str = debtor+"  borrowed $"+str(amount)+"  from you"
        await ctx.send(each_record)


@bot.command()
async def modify(ctx: Context):
    '''
    can modify name, amount of money, or item info
    '''
    myself = find_myself(str(ctx.author))
    if myself.name == "":
        await ctx.send("there is no user data of you."
                       "if you want to register, please type`$new`")
        return

    # checkUserExist()
    # [1]=the thing that want to modify,[2]= userID,[3]= amount,[4]=info
    command: list = (str(ctx.message.content)).split()
    if len(command) != 5:
        await ctx.send("there are some information missing, please type the instruction again")
        return

    whatever = ""  # store name or amount or info
    message, index = search(command[2], int(command[3]),
                            command[4], command[1], myself)

    await ctx.send(message)
    if index < 0:
        return

    try:
        answer: Message = await bot.wait_for('message', timeout=10.0)
    except asyncio.TimeoutError:
        await ctx.send("out of the time, please try again from the beginning")
    else:
        # check if the second message was sent by the same person
        #      second message      first message
        while answer.author != ctx.message.author:
            try:
                answer: Message = await bot.wait_for('message', timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.send("out of the time, please try again from the beginning")
            else:
                whatever = str(answer.content)

        whatever = str(answer.content)

    if command[1] == "-m":
        whatever = int(whatever)

    await ctx.send(replace(index, command[1], whatever, myself))


@bot.command()
async def remove(ctx: Context):
    '''
    to remove a certain record
    '''
    myself = find_myself(str(ctx.author))
    if myself.name == "":
        await ctx.send("there is no user data of you."
                       "if you want to register, please type`$new`")
        return

    # [1]=name,[2]=amount,[3]=info
    command: list = (str(ctx.message.content)).split()
    if len(command) != 4:
        await ctx.send("there are some information missing, please type the instruction again")
        return

    # remove from records
    for i, user in enumerate(myself.records):
        if user.debtor == command[1] and user.amount == int(command[2]) and user.info == command[3]:
            # modify $check
            myself.debtors[user.debtor] -= user.amount
            myself.records.pop(i)
            await ctx.send("remove successfully")
            return

    await ctx.send("there is no data")


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

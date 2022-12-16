from os import environ

from discord.ext import commands
from discord.ext.commands import Context
from discord import Message
import discord
import datetime
import asyncio


class Record:
    def __init__(self, name: str = "", debtor: str = "", date: str = "", amount: int = 0, info: str = ""):
        self._name: str = name          # username
        self._debtor: str = debtor      # debtor who borrow money from you
        self._date: str = date          # the date that event happened
        self._amount: int = amount      # how much you lent him or her
        self._info: str = info          # the info of the item

    def printRecord(self):
        print(self._date+"  $"+str(self._amount)+"  "+self._info +
              "  "+self._debtor+" borrowed from "+self._name)


class User:
    def __init__(self, name: str = "", userID: str = ""):
        self._name = name                      # username
        self._userID = userID                  # user ID in discord
        # for all the debtors and the total money of each
        self._debtors: dict[str, int] = dict()
        self._records: list[Record] = list()           # store all the records

    def append_record(self, record: Record):
        if (record._debtor in self._debtors):
            self._debtors[record._debtor] += record._amount
        else:
            self._debtors[record._debtor] = record._amount

        self._records.append(record)


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
allUsers: list[User] = list()  # store all the Users


def saveRecord(record: Record, allUsers: list):  # append a record for a certain user
    for i in range(len(allUsers)):
        if (allUsers[i]._name == record._name):
            allUsers[i].append_record(record)
            return (record._date+"  $"+str(record._amount)+"  "+record._info+"  "+record._debtor+" borrowed from "+allUsers[i]._userID)


def search(debtor: str, amount: int, info: str, thing: str, name: str):
    myself = User()
    for i in range(len(allUsers)):
        if (allUsers[i]._name == name):
            myself = allUsers[i]
            break

    # if have not account
    if (myself._name == ""):
        return ("there is no user data of you.\nif you want to register, please type\"$new\""), -99

    for i in range(len(myself._records)):
        if (myself._records[i]._debtor == debtor and myself._records[i]._amount == amount and myself._records[i]._info == info):
            if (thing == "-n"):
                return "please type new name for modifying", i
            elif (thing == "-m"):
                return "please type new amount of money for modifying", i
            elif (thing == "-i"):
                return "please type new info for modifying", i
            break

    return "have no data that you mentioned", -99


def replace(name: str, index: int, thing: str, newThing):
    myself: int = 0
    for i in range(len(allUsers)):
        if (allUsers[i]._name == name):
            myself = i
            break

    if (thing == "-n"):
        allUsers[myself]._records[index]._debtor = str(newThing)
    elif (thing == "-m"):
        allUsers[myself]._records[index]._amount = int(newThing)
    elif (thing == "-i"):
        allUsers[myself]._records[index]._info = str(newThing)

    return (allUsers[myself]._records[index]._date+"  $"+str(allUsers[myself]._records[index]._amount)+"  "+allUsers[myself]._records[index]._info+"  "+allUsers[myself]._records[index]._debtor+" borrowed from "+allUsers[myself]._userID)


@bot.command()
async def new(ctx: Context):
    for i in range(len(allUsers)):
        if (allUsers[i]._name == str(ctx.author)):
            await ctx.send("the account is already exist")
            return

    newUser: User = User(str(ctx.author), "<@"+str(ctx.author.id)+">")
    allUsers.append(newUser)

    message: str = newUser._userID + " is the new user, the whole name is "+newUser._name
    await ctx.send(message)


@bot.command()
async def record(ctx: Context):
    # command[1] = userID, command[2]=amount of money, command[3]= info
    command: list = (str(ctx.message.content)).split()

    # check if the second is userID
    if not (str(command[1])[:2] == "<@" and str(command[1][-1]) == ">"):
        await ctx.send("please tag the user to store the information of debtor")
        return

    # check if the third is int
    amountISint: bool = True
    try:
        int(command[2])
    except ValueError:
        amountISint = False

    if (amountISint == False):
        await ctx.send("the amount of money is invalid")
        return

    # if all fine
    newRecord: Record = Record(str(ctx.author), command[1], str(
        datetime.date.today()), int(command[2]), str(command[3]))
    await ctx.send(saveRecord(newRecord, allUsers))


@bot.command()
async def check(ctx: Context):
    myself: User = User()

    for i in range(len(allUsers)):
        if (allUsers[i]._name == str(ctx.author)):
            myself = allUsers[i]
            break

    # if have not account
    if (myself._name == ""):
        await ctx.send("there is no user data of you.\nif you want to register, please type\"$new\"")
        return

    # if have no debtors
    if (len(myself._debtors) == 0):
        await ctx.send("there is no debtors")
        return

    # if all fine
    for debtor, amount in myself._debtors.items():
        record: str = debtor+"  borrowed $"+str(amount)+"  from you"
        await ctx.send(record)


@bot.command()
async def modify(ctx: Context):
    # checkUserExist()
    # [1]=the thing that want to modify,[2]= userID,[3]= amount,[4]=info
    command: list = (str(ctx.message.content)).split()
    whatever = ""  # store name or amount or info
    message, index = search(command[2], int(command[3]),
                            command[4], command[1], str(ctx.author))

    await ctx.send(message)
    if (index < 0):
        return

    try:
        answer: Message = await bot.wait_for('message', timeout=10.0)
    except asyncio.TimeoutError:
        await ctx.send("out of the time, please try again from the beginning")
    else:
        # check if the second message was sent by the same person
        #      second message      first message
        while (answer.author != ctx.message.author):
            try:
                answer: Message = await bot.wait_for('message', timeout=10.0)
            except asyncio.TimeoutError:
                await ctx.send("out of the time, please try again from the beginning")
            else:
                # m = answer.content+"1"
                # await ctx.send(m)
                whatever = str(answer.content)

        # print(answer.content, ctx.message.content)

        # m = answer.content+"2"
        # await ctx.send(m)
        whatever = str(answer.content)

    if (command[1] == "-m"):
        whatever = int(whatever)

    await ctx.send(replace(str(ctx.author), index, command[1], whatever))


@bot.command()
async def remove(ctx: Context):

    ...


@bot.command()
async def how(ctx: Context):
    new = "```yaml\n$new\n```\nfor register to a new user, just type \"$new\"\n"
    record = "```yaml\n$record\n```\nfor appending a new record of you lent other people money,type\n\n$record @user Money item\nfor example, $record @you-owe-me-money 100 dinner\n"
    check = "```yaml\n$check\n```\nfor checking the total amount money of each person who had borrowed from you, just type \"$check\"\n"
    modify = "```yaml\n$modify\n```on progressing\n"
    remove = "```yaml\n$repay\n```on progressing\n"
    total = new+record+check+modify+remove
    await ctx.send(total)


bot.run(environ["TOKEN"])

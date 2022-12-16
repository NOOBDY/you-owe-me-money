from os import environ

from discord.ext import commands
from discord.ext.commands import Context
from discord import Message
import discord
import datetime


class Record:
    def __init__(self, name: str = "", debtor: str = "", date: str = "", amount: int = 0, info: str = ""):
        self._name = name          # username
        self._debtor = debtor      # debtor who borrow money from you
        self._date = date          # the date that event happened
        self._amount = amount      # how much you lent him or her
        self._info = info          # the info of the item


class User:
    def __init__(self, name: str = "", userID: str = ""):
        self._name = name                      # username
        self._userID = userID                  # user ID in discord
        # for all the debtors and the total money of each
        self._debtors: dict[str, int] = dict()
        self._records: list = list()           # store all the records

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


@bot.command()
async def new(ctx: Context):
    for i in range(len(allUsers)):
        if (allUsers[i]._name == str(ctx.author)):
            await ctx.send("the account is already exist")
            return

    newUser: User = User(str(ctx.author), "<@"+str(ctx.author.id)+">")
    allUsers.append(newUser)

    message = newUser._userID + " is the new user, the whole name is "+newUser._name
    await ctx.send(message)


@bot.command()
async def record(ctx: Context):
    # command[1] = userID, command[2]=amount of money, command[3]= info
    command = (str(ctx.message.content)).split()

    # check if the second is userID
    if not (str(command[1])[:2] == "<@" and str(command[1][-1]) == ">"):
        await ctx.send("please tag the user to store the information of debtor")
        return

    # check if the third is int
    amountISint = True
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

    if (len(myself._debtors) == 0):
        await ctx.send("there is no debtors")

    for debtor, amount in myself._debtors.items():
        record = debtor+"  borrowed $"+str(amount)+"  from you"
        await ctx.send(record)


@bot.command()
async def how(ctx: Context):
    new = "```yaml\n$new\n```\nfor register to a new user, just type \"$new\"\n"
    record = "```yaml\n$record\n```\nfor appending a new record of you lent other people money,type\n\n$record @user Money item\nfor example, $record @you-owe-me-money 100 dinner\n"
    check = "```yaml\n$check\n```\nfor checking the total amount money of each person who had borrowed from you, just type \"$check\"\n"
    modify = "```yaml\n$modify\n```on progressing\n"
    repay = "```yaml\n$repay\n```on progressing\n"
    total = new+record+check+modify+repay
    await ctx.send(total)


bot.run(environ["TOKEN"])

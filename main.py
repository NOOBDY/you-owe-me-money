from os import environ

import discord


class UserData:
    _myself = ""  # username
    _debtors = dict()  # for all the debtor and the total money of each
    _records = list()


class Record:
    _myself = ""  # username
    _debtor = ""  # debtor who borrow money from you
    _date = ""  # the date that event happened
    _amount = 0  # how much you lent him or her
    _info = ""  # the info of the item

    def __init__(self, debtor, date, amount, info):
        self._debtor = debtor
        self._date = date
        self._amount = amount
        self._info = info


def setUpUser():  # set a new record for a user
    print("setup here")


def newRecord(command, myself):  # append a record for a certain user
    temp = command.split()
    myself = "<@"+str(myself)+">"
    new = Record(temp[1], temp[2], temp[3], temp[4])
    send = new._debtor+" borrowed "+str(new._amount)+" from " + myself + " because of  " + \
        new._info+" on "+new._date
    return send


def modify():  # modify the record
    print("modify here")


def remove():  # remove the record
    print("remove here")


def check():  # print the debt data
    print("check here")


if __name__ == "__main__":
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):
        command = ""
        if (message.author == client.user):
            return

        print(message)
        print("======================\n")
        print(message.content)

        if (message.content[0:6] == "record"):
            command = message.content
            await message.channel.send(newRecord(command, message.author.id))

        if (message.content[:4] == ("new")):
            await message.channel.send("on progressing function new")

        if (message.content[:6] == ("modify")):
            await message.channel.send("on progressing function modify")

        if (message.content[:6] == ("remove")):
            await message.channel.send("on progressing function remove")

        if (message.content[:5] == ("check")):
            await message.channel.send("on progressing function check")

    # client.run(environ["DISCORD_BOT_TOKEN"]
    client.run(
        "MTA1MTAyMTc5NjM0ODAwNjQ1MQ.G2pzRn.caXY2YiXIoXEuBCUxfyaVXquPsB6WrPg9Jrcz4")

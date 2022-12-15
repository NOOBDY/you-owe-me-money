from os import environ

import discord


class UserData:
    _myself = ""  # username
    _userID = ""  # user ID in discord
    _debtors = dict()  # for all the debtor and the total money of each
    _records = list()  # store all the records

    def __init__(self, myself, userID):
        self._myself = myself
        self._userID = userID

    def append_record(self, debtor, money, record):
        if (debtor in self._debtors):
            self._debtors[debtor] += int(money)
        else:
            self._debtors[debtor] = int(money)

        self._records.append(record)


class Record:
    _myself = ""  # username
    _debtor = ""  # debtor who borrow money from you
    _date = ""  # the date that event happened
    _amount = 0  # how much you lent him or her
    _info = ""  # the info of the item

    def __init__(self, myself, debtor, date, amount, info):
        self._myself = myself
        self._debtor = debtor
        self._date = date
        self._amount = amount
        self._info = info


def setUpUser(name, ID, allUsers):  # set a new record for a user
    for i in range(len(allUsers)):
        if (allUsers[i]._myself == str(name)):
            return ("account is already existed")

    newUser = UserData(str(name), "<@"+str(ID)+">")
    send = newUser._userID + " is the new user, the whole name is "+newUser._myself
    allUsers.append(newUser)
    return send


def newRecord(command, myself, allUsers):  # append a record for a certain user
    temp = command.split()
    new = Record("<@"+str(myself)+">", temp[1], temp[2], temp[3], temp[4])
    send = new._date+"  $"+str(new._amount)+"  " + \
        new._info + "  " + new._debtor + " borrowed from " + new._myself

    for i in range(len(allUsers)):
        if (allUsers[i]._userID == new._myself):
            allUsers[i].append_record(new._debtor, new._amount, new)
            break

    return send


def modify(command, myself):  # modify the record
    temp = command.split()
    if (temp[1] == "-name"):
        ...
    elif (temp[1] == "-date"):
        ...
    elif (temp[1] == "sum"):
        ...
    elif (temp[1] == "info"):
        ...

    return ("modified successfully")


def remove():  # remove the record
    print("remove here")


def check():  # print the debt data
    print("check here")


if __name__ == "__main__":
    allUsers = list()  # store all the UserData

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):

        # print(message)

        if (message.author == client.user):
            return

        if (message.content[:6] == "record"):
            # command = message.content
            await message.channel.send(newRecord(message.content, message.author.id, allUsers))

        if (message.content[:4] == ("new")):
            await message.channel.send(setUpUser(message.author, message.author.id, allUsers))

        if (message.content[:6] == ("modify")):
            await message.channel.send(modify(message.content, message.author.id))

        if (message.content[:6] == ("remove")):
            await message.channel.send("on progressing function remove")

        if (message.content[:5] == ("check")):
            await message.channel.send("on progressing function check")

        # check if the data is stored
        for item in range(len(allUsers)):
            await message.channel.send(allUsers[item]._myself)
            for r in range(len(allUsers[item]._records)):
                await message.channel.send(allUsers[item]._records[r]._debtor)
                await message.channel.send(allUsers[item]._records[r]._date)
                await message.channel.send(allUsers[item]._records[r]._amount)
                await message.channel.send(allUsers[item]._records[r]._info)
                await message.channel.send("--------------------------------")

            await message.channel.send(allUsers[item]._debtors[allUsers[item]._records[0]._debtor])

    client.run(environ["TOKEN"])

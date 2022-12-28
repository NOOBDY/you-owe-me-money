from os import environ

import db

import discord

if __name__ == "__main__":
    db.find_record(123)

    data = db.Record(345, 420, 1200, "gatcha")

    db.add_record(data)

    db.find_record(345)
    exit(0)

    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"We have logged in as {client.user}")

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith("$hello"):
            await message.channel.send("Hello!")

    client.run(environ["DISCORD_BOT_TOKEN"])

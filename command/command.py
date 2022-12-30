"""
command module
"""

from discord.ext.commands import Context
from discord.ext import commands


@commands.command()
async def add(ctx: Context):
    """
    Usage: `add <debtor-id> <amount> <title> [detail]`

    Description: Adds a new record into the database.
    """


@commands.command()
async def remove(ctx: Context):
    """
    Usage: `remove <record-id>`

    Description: Removes a record from the database by querying the record ID.
    """


@commands.command()
async def modify(ctx: Context):
    """
    Usage: `modify <record-id> <name|amount|info> <value>`

    Description: Modify the specified value in the database.
    """


@commands.command()
async def clear(ctx: Context):
    """
    Usage: `clear <record-id>`

    Description: Clear the record but not delete it from the database
    """

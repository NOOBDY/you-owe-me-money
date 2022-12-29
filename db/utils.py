"""
utils module
"""

from .record import Record


def add_record(record: Record) -> None:
    '''
    add a certain record to a user data
    '''
    ...


def delete_record(record_id: int) -> None:
    ''' 
    delete a certain record of a user data
    '''
    ...


def find_record(record_id: int) -> Record:
    '''
    find a certain record of a user data
    '''
    ...


def creditor_records(creditor_id: int) -> list[Record]:
    '''
    i don't know what it is
    to put a certain user's record to a list?
    '''
    ...


def debtor_records(debtor_id: int) -> list[Record]:
    '''
    i don't know what it is
    to put a certain debtor's record to a list?
    '''
    ...

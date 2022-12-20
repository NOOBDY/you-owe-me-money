"""
utils module
"""

from .record import Record


def add_record(record: Record) -> None:
    ...


def delete_record(record_id: int) -> None:
    ...


def find_record(record_id: int) -> Record:
    ...


def creditor_records(creditor_id: int) -> list[Record]:
    ...


def debtor_records(debtor_id: int) -> list[Record]:
    ...

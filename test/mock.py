"""
mock module
"""

import uuid

from db.record import Record


# This uses a global variable to emulate a DB
MOCK_DB: dict[int, Record] = {}


def reset() -> None:
    MOCK_DB.clear()

    records = [
        Record(69, 420, 1200, "gatcha"),
        Record(234, 420, 1, "nice"),
        Record(69, 234, 60, "unit test"),
    ]

    for record in records:
        add_record(record)


def add_record(record: Record) -> None:
    MOCK_DB[uuid.uuid1().int] = record


def delete_record(record_id: int) -> None:
    del MOCK_DB[record_id]


def find_record(record_id: int) -> Record:
    return MOCK_DB[record_id]


def list_records() -> dict[int, Record]:
    return MOCK_DB


def creditor_records(creditor_id: int) -> dict[int, Record]:
    return dict(filter(
        lambda x: x[1].get_creditor_id() == creditor_id,
        MOCK_DB.items()
    ))


def debtor_records(debtor_id: int) -> dict[int, Record]:
    return dict(filter(
        lambda x: x[1].get_debtor_id() == debtor_id,
        MOCK_DB.items()
    ))

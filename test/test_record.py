"""
test record
"""

from db.record import Record

from .mock import (add_record, delete_record, list_records, reset)


def test_update_record():
    """
    testing `add_record` and `delete_record`
    """
    reset()

    add_record(Record(1, 2, 45, "alcohol"))

    all_records = list_records()

    delete_record(list(all_records.keys())[2])

    target_records = [
        Record(69, 420, 1200, "gatcha"),
        Record(234, 420, 1, "nice"),
        Record(1, 2, 45, "alcohol")
    ]

    assert all([x in list(all_records.values()) for x in target_records])

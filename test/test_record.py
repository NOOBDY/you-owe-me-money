"""
test record
"""

from db.record import Record

from .mock_utils import (add_record, delete_record, list_records, reset)


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

    for record in target_records:
        assert record in list(all_records.values())


def test_reset():
    """
    test if `reset` works or not
    """

    reset()

    target_records = [
        Record(69, 420, 1200, "gatcha"),
        Record(234, 420, 1, "nice"),
        Record(69, 234, 60, "unit test"),
    ]

    all_records = list_records()

    assert len(all_records) == 3

    for record in target_records:
        assert record in list(all_records.values())

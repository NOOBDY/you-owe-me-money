from db.utils import add_record, creditor_records, delete_record
from db.record import Record


def test_upload():
    data = Record(345, 420, 1200, "gatcha")
    before = creditor_records(345)
    add_record(data)
    after = creditor_records(345)
    assert len(before) == len(after)-1


def test_delete():
    data = Record(345, 420, 1200, "gatcha")
    before = creditor_records(345)
    add_record(data)
    after = creditor_records(345)
    assert len(before) == len(after)-1

    before = creditor_records(345)
    delete_record(after[-1].get_record_id())
    after = creditor_records(345)
    assert len(before) == len(after)+1



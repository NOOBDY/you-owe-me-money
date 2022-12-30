from db.utils import add_record, creditor_records, delete_record,update_records
from db.record import Record
from datetime import date

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
def test_update():
    data = Record(345, 420, 1200, "gatcha")
    add_record(data)
    before = creditor_records(345)
    before[-1].clear()
    update_records(before[-1])
    after = find_record(before[-1].get_record_id())
    assert after.__dict__["_cleared_on"] == str(date.today())


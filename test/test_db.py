from db.utils import add_record,creditor_records
from db.record import Record
def Test_Upload(recoder:Record):
    data = Record(69, 420, 1200, "gatcha")
    add_record(data)
    creditor_record = creditor_records(69)
    print(creditor_records)
    

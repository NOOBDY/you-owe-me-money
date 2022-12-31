"""
utils module
"""
from os import environ

from supabase.client import Client

from db.record import Record


url = environ["SUPABASE_URL"]
key = environ["SUPABASE_API_KEY"]
supabase = Client(url, key)

table = "Prod Record"


def add_record(record: Record) -> None:
    supabase.table(table).insert(record.to_dict()).execute()


def delete_record(record_id: int) -> None:
    (supabase.table(table)
     .delete()
     .filter("record_id", "eq", str(record_id))
     .execute())


def find_record(record_id: int) -> Record:
    try:
        res = supabase.table(table).select("*").filter("record_id", "eq", str(record_id)).execute().data
        print(res)
        if len(res) == 0:
            return None
        return dict_to_record(res[0])
    except:
        pass
    return None


def creditor_records(creditor_id: int) -> list[Record]:
    return [dict_to_record(temp) for temp in supabase.table(table)
            .select("*")
            .filter("creditor_id", "eq", str(creditor_id))
            .execute()
            .data]


def debtor_records(debtor_id: int) -> list[Record]:
    return [dict_to_record(temp) for temp in supabase.table(table)
            .select("*")
            .filter("debtor_id", "eq", str(debtor_id))
            .execute()
            .data]


def update_record(record: Record) -> None:
    (supabase.table(table)
     .update(record.to_dict_full())
     .filter("record_id", "eq", str(record.get_record_id()))
     .execute())


def dict_to_record(data):  # 轉換成record格式
    return Record(
        data["creditor_id"],
        data["debtor_id"],
        data["amount"],
        data["title"],
        data["detail"],
        data["due_date"],
        data["record_id"],
        data["created_on"],
        data["cleared_on"],
        data["modified_on"]
    )

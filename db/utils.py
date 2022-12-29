"""
utils module
"""
from os import environ

from supabase.client import Client

from db.record import Record

url = environ["SUPABASE_URL"]
key = environ["SUPABASE_API_KEY"]
supabase = Client(url, key)

TABLE = "Test Record"


def add_record(record: Record) -> None:
    try:
        supabase.table(TABLE).insert(record.record_to_dict()).execute()
    except Exception as e:
        print(e)
    return None


def delete_record(record_id: int) -> None:
    try:
        supabase.table(TABLE).delete().filter("record_id", "eq", str(record_id)).execute()
    except:
        pass
    return None


def find_record(record_id: int) -> Record:
    try:
        res = supabase.table(TABLE).select("*").filter("record_id", "eq", str(record_id)).execute().data
        print(res)
        if len(res) == 0:
            return None
        return dict_to_record(res[0])
    except:
        pass
    return None


def creditor_records(creditor_id: int) -> list[Record]:
    try:
        return [dict_to_record(temp) for temp in
                supabase.table(TABLE).select("*").filter("creditor_id", "eq", str(creditor_id)).execute().data]
    except:
        pass
    return None


def debtor_records(debtor_id: int) -> list[Record]:
    try:
        return [dict_to_record(temp)for temp in supabase.table("Record").select("*").filter("debtor_id", "eq", debtor_id).execute().data]
    except:
        pass
    return None


def update_records(record: Record) -> None:
    try:
        supabase.table(TABLE).update(record.record_to_dict_full()).filter("record_id", "eq", record.get_record_id()).execute()
    except:
        pass
    return None


def dict_to_record(data):  # 轉換成record格式
    creditor_id = data["creditor_id"]
    debtor_id = data["debtor_id"]
    amount = data["amount"]
    title = data["title"]
    detail = data["detail"]
    due_date = data["due_date"]
    record_id = data["record_id"]
    created_on = data["created_on"]
    cleared_on = data["cleared_on"]
    modified_on = data["modified_on"]
    return Record(creditor_id, debtor_id, amount, title, detail, due_date, record_id, created_on, cleared_on, modified_on)

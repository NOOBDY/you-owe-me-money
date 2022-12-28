"""
utils module
"""
from os import environ
from db.record import Record
from supabase import create_client,Client

url = environ["SUPABASE_URL"]
key = environ["SUPABASE_API_KEY"]
supabase = create_client(url, key)

def add_record(record: Record) -> None:
    try:
        supabase.table("Record").insert(record.RecordToDict()).execute()
    except:
        pass
    return None

def delete_record(record_id: int) -> None:
    try:
        supabase.table("Record").delete().filter("record_id", "eq", record_id).execute()
    except:
        pass
    return None

def find_record(record_id: int) -> Record:
    try:
        res = supabase.table("Record").select("*").filter("record_id", "eq", record_id).execute().data
        if len(res)==0:
            return None
        return DictToReocrd(res[0])
    except:
        pass
    return None

def creditor_records(creditor_id: int) -> list[Record]:
    try:
        return [DictToReocrd(temp)for temp in supabase.table("Record").select("*").filter("creditor_id", "eq",creditor_id).execute().data]
    except:
        pass
    return None

def debtor_records(debtor_id: int) -> list[Record]:
    try:
        return [DictToReocrd(temp)for temp in supabase.table("Record").select("*").filter("debtor_id", "eq", debtor_id).execute().data]
    except:
        pass
    return None


def DictToReocrd(data):  # 轉換成record格式
    creditor_id = data["creditor_id"]
    debtor_id = data["debtor_id"]
    amount = data["amount"]
    title = data["title"]
    detail = data["detail"]
    due_date = data["due_date"]
    record_id = data["record_id"]
    return Record(creditor_id, debtor_id,amount, title, detail,due_date,record_id)
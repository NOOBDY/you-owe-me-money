"""
utils module
"""
from os import environ
from .record import Record
url: str = "https://dwosibtkxkverqqwtsnp.supabase.co"
key: str = environ["SUPABASE_API_KEY"]
supabase: Client = create_client(url, key)

def add_record(record: Record) -> None:
    try:
        supabase.table("Record").insert(record.RecordToDict()).execute()
    except:
        pass


def delete_record(record_id: int) -> None:
    ...


def find_record(record_id: int) -> Record:
    ...


def creditor_records(creditor_id: int) -> list[Record]:
    ...


def debtor_records(debtor_id: int) -> list[Record]:
    ...

def IsCheckid(id)->bool:
    return len(supabase.table("Record").select("*").filter("record_id", "eq", key).execute().data)!=0
"""
utils module
"""
from os import environ
from .record import Record
from supabase import create_client,Client

url = environ["SUPABASE_URL"]
key = environ["SUPABASE_API_KEY"]
Client = create_client(url, key)

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
        return supabase.table("Record").select("*").filter("record_id", "eq", record_id).execute()
    except:
        pass
    return None    

def creditor_records(creditor_id: int) -> list[Record]:
    try:
        return supabase.table("Record").select("*").filter("creditor_id", "eq",creditor_id).execute()
    except:
        pass
    return None

def debtor_records(debtor_id: int) -> list[Record]:
    try:
        return supabase.table("Record").select("*").filter("debtor_id", "eq", debtor_id).execute()
    except:
        pass
    return None    



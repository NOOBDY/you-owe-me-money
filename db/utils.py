"""
utils module
"""

from typing import Any
from os import environ

from supabase.client import Client

from db.record import Record


url = environ["SUPABASE_URL"]
key = environ["SUPABASE_API_KEY"]
supabase = Client(url, key)

TABLE = environ["SUPABASE_TABLE"]


def add_record(record: Record) -> None:
    supabase.table(TABLE).insert(record.to_dict()).execute()


def delete_record(record_id: int) -> None:
    (supabase.table(TABLE)
     .delete()
     .filter("record_id", "eq", str(record_id))
     .execute())


def find_record(record_id: int) -> Record | None:
    records: list[dict[str, Any]] = (supabase.table(TABLE)
                                     .select("*")
                                     .filter("record_id", "eq", str(record_id))
                                     .execute()
                                     .data)

    if len(records) == 0:
        return None

    return dict_to_record(records[0])


def creditor_records(creditor_id: int) -> list[Record]:
    return [dict_to_record(temp) for temp in supabase.table(TABLE)
            .select("*")
            .filter("creditor_id", "eq", str(creditor_id))
            .filter("cleared_on", "is", "null")
            .execute()
            .data]


def debtor_records(debtor_id: int) -> list[Record]:
    return [dict_to_record(temp) for temp in supabase.table(TABLE)
            .select("*")
            .filter("debtor_id", "eq", str(debtor_id))
            .filter("cleared_on", "is", "null")
            .execute()
            .data]


def update_record(record: Record) -> None:
    (supabase.table(TABLE)
     .update(record.to_dict_full())
     .filter("record_id", "eq", str(record.get_record_id()))
     .execute())


def dict_to_record(data: dict[str, Any]):  # 轉換成record格式
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

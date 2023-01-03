"""
record module
"""

from typing import Any

from datetime import date


class Record:
    """
    # Record class

    This class is a basic wrapper around the SQL database
    """

    def __init__(self, creditor_id: int, debtor_id: int,
                 amount: int, title: str, detail: str = "",
                 due_date: str | None = None,
                 record_id: int | None = None,
                 created_on: str = str(date.today()),
                 cleared_on: str | None = None,
                 modified_on: str | None = None):
        self._creditor_id = creditor_id
        self._debtor_id = debtor_id
        self._amount = amount
        self._title = title
        self._detail = detail
        self._due_date = due_date
        self._record_id = record_id
        self._created_on = created_on
        self._cleared_on = cleared_on
        self._modified_on = modified_on if modified_on else created_on

    def get_creditor_id(self) -> int:
        return self._creditor_id

    def get_debtor_id(self) -> int:
        return self._debtor_id

    def get_amount(self) -> int:
        return self._amount

    def get_title(self) -> str:
        return self._title

    def get_detail(self) -> str:
        return self._detail

    def get_due_date(self) -> str | None:
        return self._due_date

    def get_record_id(self) -> int:
        return self._record_id if self._record_id else -1

    def set_debtor_id(self, debtor_id: int) -> None:
        self._debtor_id = debtor_id

    def set_amount(self, amount: int) -> None:
        self._amount = amount

    def set_title(self, title: str) -> None:
        self._title = title

    def set_detail(self, detail: str) -> None:
        self._detail = detail

    def set_due_date(self, due_date: str | None) -> None:
        self._due_date = due_date

    def clear(self) -> None:
        self._cleared_on = str(date.today())

    def to_dict(self):  # 轉換成資料庫上傳格式
        data = self.__dict__
        res: dict[str, Any] = {key[1:]: value for key, value in data.items()}
        res.pop('record_id')
        res.pop('created_on')
        res.pop('due_date')
        res.pop('modified_on')
        res.pop('cleared_on')
        return res

    def to_dict_full(self):  # 轉換成資料庫上傳格式
        return {key[1:]: value for key, value in self.__dict__.items()}

    def to_discord_message(self):
        return (f"{self._modified_on} {self._amount} {self._title}"
                f"<@{self._debtor_id}> borrowed from <@{self._creditor_id}>")

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__

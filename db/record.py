"""
record module
"""

from datetime import date, datetime


class Record:
    """
    # Record class

    This class is a basic wrapper around the SQL database
    """

    def __init__(self, creditor_id: int, debtor_id: int,
                 amount: int, title: str, detail: str = "",
                 due_date: datetime | None = None, record_id: str = None, created_on: str = None, cleared_on: str = None, modified_on: str = None):
        self._creditor_id = creditor_id
        self._debtor_id = debtor_id
        self._amount = amount
        self._title = title
        self._detail = detail
        self._due_date = due_date
        self._record_id = record_id
        self._created_on = created_on
        self._cleared_on = cleared_on
        self._modified_on = modified_on

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

    def get_due_date(self) -> datetime | None:
        return self._due_date

    def get_record_id(self) -> int:
        return self._record_id

    def set_debtor_id(self, debtor_id: int) -> None:
        self._debtor_id = debtor_id

    def set_amount(self, amount: int) -> None:
        self._amount = amount

    def set_title(self, title: str) -> None:
        self._title = title

    def set_detail(self, detail: str) -> None:
        self._detail = detail

    def set_due_date(self, due_date: datetime | None) -> None:
        self._due_date = due_date

    def clear(self) -> None:
        self._cleared_on = str(date.today())

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__

    def RecordToDict(self):  # 轉換成資料庫上傳格式
        data = self.__dict__
        p = dict()
        for key in data:
            p[key[1:]] = data[key]
        p.pop('record_id')
        p.pop('created_on')
        p.pop('due_date')
        p.pop('modified_on')
        p.pop('cleared_on')
        return p

    def RecordToDictFull(self):  # 轉換成資料庫上傳格式
        data = self.__dict__
        p = dict()
        for key in data:
            p[key[1:]] = data[key]
        return p

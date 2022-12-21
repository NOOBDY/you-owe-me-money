"""
record module
"""

from datetime import datetime


class Record:
    """
    # Record class

    This class is a basic wrapper around the SQL database
    """

    def __init__(self, creditor_id: int, debtor_id: int,
                 amount: int, title: str, detail: str = "",
                 due_date: datetime | None = None):
        self._creditor_id = creditor_id
        self._debtor_id = debtor_id
        self._amount = amount
        self._title = title
        self._detail = detail
        self._due_date = due_date

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

    def set_debtor_id(self, debtor_id: int) -> None:
        self._debtor_id = debtor_id

    def set_amount(self, amount: int) -> None:
        self._amount = amount

    def set_title(self, title: str) -> None:
        self._title = title

    def set_detail(self, detail: str) -> None:
        self._detail = detail

    def set_due_date(self, due_date: datetime) -> None:
        self._due_date = due_date

    def apply_update(self) -> None:
        ...

    def clear(self) -> None:
        ...

    def __eq__(self, __o: object) -> bool:
        return self.__dict__ == __o.__dict__

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
        ...

    def update_debtor(self, debtor_id: int) -> None:
        ...

    def update_amount(self, amount: int) -> None:
        ...

    def update_title(self, title: str) -> None:
        ...

    def update_detail(self, detail: str) -> None:
        ...

    def update_due_date(self, due_date: datetime) -> None:
        ...

    def apply_update(self) -> None:
        ...

    def clear(self) -> None:
        ...

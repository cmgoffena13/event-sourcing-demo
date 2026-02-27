from decimal import Decimal

from eventsourcing.domain import Aggregate, event
from pydantic import EmailStr


class Account(Aggregate):
    @event("Created")
    def __init__(self, email: EmailStr) -> None:
        self.email: EmailStr = email
        self.balance: Decimal = Decimal(0.00)
        self.is_closed: bool = False

    @event("Deposited")
    def deposit(self, amount: Decimal) -> None:
        self.balance += amount

    @event("Withdrawed")
    def withdraw(self, amount: Decimal) -> None:
        self.balance -= amount

    @event("Closed")
    def close(self) -> None:
        self.is_closed = True

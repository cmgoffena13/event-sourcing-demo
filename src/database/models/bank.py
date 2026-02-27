from decimal import Decimal
from typing import Annotated
from uuid import UUID

from eventsourcing.application import Application
from fastapi import Depends
from pydantic import EmailStr

from src.database.models.account import Account


class Bank(Application[UUID]):
    def create_account(self, email: EmailStr) -> UUID:
        account = Account(email=email)
        self.save(account)
        return account.id

    def get_account(self, account_id: UUID) -> Decimal:
        account = self.repository.get(account_id)
        return account

    def deposit(self, account_id: UUID, amount: Decimal) -> None:
        account = self.repository.get(account_id)
        account.deposit(amount)
        self.save(account)

    def withdraw(self, account_id: UUID, amount: Decimal) -> None:
        account = self.repository.get(account_id)
        account.withdraw(amount)
        self.save(account)

    def close_account(self, account_id: UUID) -> None:
        account = self.repository.get(account_id)
        account.close()
        self.save(account)


async def get_bank() -> Bank:
    yield Bank()


ApplicationDep = Annotated[Bank, Depends(get_bank)]

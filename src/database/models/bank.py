from decimal import Decimal
from typing import Annotated
from uuid import UUID

from eventsourcing.application import Application
from fastapi import Depends
from pydantic import EmailStr

from src.database.models.account import Account
from src.database.models.transfer import Transfer


class Bank(Application[UUID]):
    # Snapshot every 2 events per aggregate so you can see snapshot logic (e.g. in SQL).
    snapshotting_intervals = {Account: 2, Transfer: 2}

    def create_account(self, email: EmailStr) -> UUID:
        account = Account(email=email)
        self.save(account)
        return account.id

    def get_account(self, account_id: UUID) -> Account:
        return self.repository.get(account_id)

    def deposit(self, account_id: UUID, amount: Decimal) -> None:
        account = self.repository.get(account_id)
        account.deposit(amount)
        self.save(account)

    def withdraw(self, account_id: UUID, amount: Decimal) -> None:
        account = self.repository.get(account_id)
        account.withdraw(amount)
        self.save(account)

    def transfer(
        self, from_account_id: UUID, to_account_id: UUID, amount: Decimal
    ) -> UUID:
        if from_account_id == to_account_id:
            raise ValueError("Source and destination accounts must differ")
        if amount <= 0:
            raise ValueError("Transfer amount must be positive")
        source = self.repository.get(from_account_id)
        dest = self.repository.get(to_account_id)
        if source.is_closed:
            raise ValueError("Source account is closed")
        if dest.is_closed:
            raise ValueError("Destination account is closed")
        if source.balance < amount:
            raise ValueError("Insufficient balance")
        transfer = Transfer(from_account_id, to_account_id, amount)
        source.transfer_out(amount, to_account_id, transfer.id)
        dest.transfer_in(amount, from_account_id, transfer.id)
        self.save(transfer, source, dest)
        return transfer.id

    def close_account(self, account_id: UUID) -> None:
        account = self.repository.get(account_id)
        account.close()
        self.save(account)


async def get_bank() -> Bank:
    yield Bank()


ApplicationDep = Annotated[Bank, Depends(get_bank)]

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, status
from pydantic import BaseModel, EmailStr

from src.database.models.bank import ApplicationDep

router = APIRouter()


class TransferRequest(BaseModel):
    from_account_id: UUID
    to_account_id: UUID
    amount: Decimal


class TransferResponse(BaseModel):
    transfer_id: UUID
    from_account_id: UUID
    to_account_id: UUID
    amount: Decimal


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
async def route_create_account(email: EmailStr, bank: ApplicationDep):
    return bank.create_account(email)


@router.get("/accounts/{account_id}", status_code=status.HTTP_200_OK)
async def route_get_account(account_id: UUID, bank: ApplicationDep):
    return bank.get_account(account_id)


@router.post("/accounts/{account_id}/deposit", status_code=status.HTTP_200_OK)
async def route_deposit(account_id: UUID, amount: Decimal, bank: ApplicationDep):
    return bank.deposit(account_id, amount)


@router.post("/accounts/{account_id}/withdraw", status_code=status.HTTP_200_OK)
async def route_withdraw(account_id: UUID, amount: Decimal, bank: ApplicationDep):
    return bank.withdraw(account_id, amount)


@router.post("/accounts/{account_id}/close", status_code=status.HTTP_200_OK)
async def route_close(account_id: UUID, bank: ApplicationDep):
    return bank.close_account(account_id)


@router.post("/transfers", status_code=status.HTTP_201_CREATED)
async def route_transfer(body: TransferRequest, bank: ApplicationDep):
    transfer_id = bank.transfer(body.from_account_id, body.to_account_id, body.amount)
    return TransferResponse(
        transfer_id=transfer_id,
        from_account_id=body.from_account_id,
        to_account_id=body.to_account_id,
        amount=body.amount,
    )

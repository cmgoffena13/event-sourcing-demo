from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, status
from pydantic import EmailStr

from src.database.models.bank import ApplicationDep

router = APIRouter()


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

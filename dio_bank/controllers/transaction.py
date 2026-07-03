from fastapi import APIRouter, Depends, status

from dio_bank.schemas.transaction import TransactionIn
from dio_bank.security import login_required
from dio_bank.services.transaction import TransactionService
from dio_bank.views.transaction import TransactionOut

# router = APIRouter(prefix='/transactions')
router = APIRouter(prefix='/transactions',
                   dependencies=[Depends(login_required)])

services = TransactionService()


@router.post(
        '/{account_id}',
        response_model=TransactionOut,
        status_code=status.HTTP_201_CREATED
    )
async def make_transaction(transaction: TransactionIn, account_id: int):
    return await services.make_transaction(transaction, account_id)


@router.get(
        '/{account_id}',
        response_model=list[TransactionOut],
        status_code=status.HTTP_200_OK
    )
async def read_transactions_by_account_id(account_id: int):
    return await services.read_transactions_by_account(account_id)


@router.get('/', response_model=list[TransactionOut], status_code=status.HTTP_200_OK)
async def read_transactions(limit: int = 10, skip: int = 0):
    return await services.read_all(limit, skip)


@router.get('/{id}', response_model=TransactionOut, status_code=status.HTTP_200_OK)
async def read_transaction_by_id(id: int):
    return await services.read(id)

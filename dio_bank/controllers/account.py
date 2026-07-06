from fastapi import APIRouter, Depends, status

from dio_bank.schemas.account import AccountIn, AccountPut
from dio_bank.security import login_required
from dio_bank.services.account import AccountService
from dio_bank.services.transaction import TransactionService
from dio_bank.views.account import AccountOut
from dio_bank.views.transaction import TransactionOut

router = APIRouter(prefix='/accounts', dependencies=[Depends(login_required)])
services = AccountService()
tx_services = TransactionService()


@router.post(
    '/', response_model=AccountOut, status_code=status.HTTP_201_CREATED
)
async def create_account(account: AccountIn):
    return await services.create(account)


@router.get(
    '/', response_model=list[AccountOut], status_code=status.HTTP_200_OK
)
async def read_accounts(limit: int = 10, skip: int = 0):
    return await services.read_all(limit, skip)


@router.get('/{id}', response_model=AccountOut, status_code=status.HTTP_200_OK)
async def read_account_by_id(id: int):
    return await services.read(id)


@router.get(
    '/{id}/transactions',
    response_model=list[TransactionOut],
    status_code=status.HTTP_200_OK,
)
async def read_account_transactions(id: int):
    return await tx_services.read_all_by_account(id)


@router.put('/{id}', response_model=AccountOut, status_code=status.HTTP_200_OK)
async def update_account(account: AccountPut, id: int):
    return await services.update(account, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(id: int):
    return await services.delete(id)

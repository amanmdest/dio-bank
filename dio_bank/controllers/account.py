from fastapi import APIRouter, Depends, status

from dio_bank.schemas.account import AccountIn, AccountPut
from dio_bank.security import login_required
from dio_bank.services.account import AccountService
from dio_bank.views.account import AccountOut

router = APIRouter(prefix='/accounts', dependencies=[Depends(login_required)])
services = AccountService()


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
async def read_by_id(id: int):
    return await services.read(id)


@router.put('/{id}', response_model=AccountOut, status_code=status.HTTP_200_OK)
async def update_account(account: AccountPut, id: int):
    return await services.update(account, id)


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(id: int):
    return await services.delete(id)

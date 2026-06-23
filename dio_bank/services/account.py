from databases.interfaces import Record

from dio_bank.database import database
from dio_bank.exceptions import NotFoundAccountError
from dio_bank.models.account import accounts
from dio_bank.schemas.account import AccountPut


class AccountService:
    async def create(self, account):
        command = accounts.insert().values(
            holder=account.holder,
            balance=account.balance,
        )
        return await database.execute(command)

    async def read_all(self, limit: int, skip: int):
        query = accounts.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def update(self, account: AccountPut, id: int):
        query = accounts.select().where(accounts.c.id == id)
        if not query:
            raise NotFoundAccountError

        data = account.model_dump(exclude_unset=True)
        command = accounts.update().where(accounts.c.id == id).values(data)

        return await database.execute(command)

    async def delete(self, id: int):
        command = accounts.delete(accounts.c.account_id == id)
        return await database.execute(command)

    async def __get_by_id(self, id: int):
        query = accounts.select().where(accounts.c.id == id)
        account = await database.fetch_one(query)
        if not account:
            raise NotFoundAccountError
        return account

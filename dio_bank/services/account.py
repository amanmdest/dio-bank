import sqlalchemy as sa
from databases.interfaces import Record

from dio_bank.database import database
from dio_bank.exceptions import NotFoundAccountError
from dio_bank.models.account import accounts
from dio_bank.schemas.account import AccountIn, AccountPut


class AccountService:
    async def create(self, account: AccountIn) -> None:
        command = accounts.insert().values(
            holder=account.holder,
            balance=account.balance
        )
        record_id = await database.execute(command)
        query = accounts.select().where(accounts.c.id == record_id)

        return await database.fetch_one(query)

    async def read_all(self, limit: int, skip: int):
        query = accounts.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def update(self, account: AccountPut, id: int):
        total = await self.count(id)
        if not total:
            raise NotFoundAccountError

        data = account.model_dump(exclude_unset=True)
        if not data:
            # Se nenhum campo foi enviado para alteração, evita ir ao banco à toa
            query = accounts.select().where(accounts.c.id == id)
            db_account = await database.fetch_one(query)
            if not db_account:
                raise NotFoundAccountError
            return db_account

        command = accounts.update().where(accounts.c.id == id).values(data)
        rows_affected = await database.execute(command)

        if rows_affected == 0:
            raise NotFoundAccountError

        query = accounts.select().where(accounts.c.id == id)
        return await database.fetch_one(query)

    async def delete(self, id: int):
        command = accounts.delete(accounts.c.account_id == id)
        return await database.execute(command)

    async def count(self, id: int) -> int:
        query = sa.select(sa.func.count(accounts.c.id)).where(accounts.c.id == id)
        result = await database.execute(query)  # returns the count integer directly
        return result

    async def __get_by_id(self, id: int):
        query = accounts.select().where(accounts.c.id == id)
        account = await database.fetch_one(query)
        if not account:
            raise NotFoundAccountError
        return account

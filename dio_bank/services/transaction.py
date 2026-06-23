from databases.interfaces import Record

from dio_bank.database import database
from dio_bank.exceptions import NotFoundAccountError, NotFoundTransactionError
from dio_bank.models.transaction import transactions
from dio_bank.schemas.transaction import TransactionIn
from dio_bank.services.account import AccountService

services = AccountService


class TransactionService:
    async def create(self, account_id: int, transaction: TransactionIn):
        # account = services.update()
        command_2 = transactions.insert().values(
            account_id=account_id,
            transaction=transaction.transaction,
            amount=transaction.amount,
        )
        # async with database.transaction():
        # await database.execute(command)

    async def read_all(self, limit: int, skip: int) -> list[Record]:
        query = transactions.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def read_by_account_id(self, account_id: int) -> list[Record]:
        return await self.__get_by_account_id(id)

    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def __get_by_account_id(self, account_id: int) -> list[Record]:
        query = transactions.select().where(
            transactions.c.account_id == account_id
        )
        print(query)
        accounts = database.fetch_all(query)
        if not accounts:
            raise NotFoundAccountError
        return accounts

    async def __get_by_id(self, id: int) -> Record:
        query = transactions.select().where(transactions.c.id == id)
        transaction = database.fetch_one(query)
        if not transaction:
            raise NotFoundTransactionError
        return transaction

from databases.interfaces import Record

from dio_bank.database import database
from dio_bank.exceptions import NotFoundAccountError, NotFoundTransactionError
from dio_bank.models.account import accounts
from dio_bank.models.transaction import transactions
from dio_bank.schemas.account import AccountPut
from dio_bank.schemas.transaction import TransactionIn
from dio_bank.services.account import AccountService

services = AccountService()


class TransactionService:
    async def make_transaction(
            self,
            transaction: TransactionIn,
            account_id: int
        ) -> None:
        query = accounts.select().where(accounts.c.id == account_id)
        account = await database.fetch_one(query)

        if not account:
            raise NotFoundAccountError

        if transaction.transaction == 'withdraw':
            if transaction.amount > account.balance:
                raise Exception('solde insuffisant')

            data = AccountPut(**{'balance': account.balance - transaction.amount})

        if transaction.transaction == 'deposit':
            data = AccountPut(**{'balance': account.balance + transaction.amount})

        await services.update(data, account_id)

        command = transactions.insert().values(
            account_id=account_id,
            transaction=transaction.transaction,
            amount=transaction.amount,
        )

        record_id = await database.execute(command)
        fetch_query = transactions.select().where(transactions.c.id == record_id)

        return await database.fetch_one(fetch_query)

    async def read_all(
            self, limit: int, skip: int
        ) -> list[Record]:
        query = transactions.select().limit(limit).offset(skip)
        return await database.fetch_all(query)

    async def read_transactions_by_account(self, account_id: int) -> list[Record]:
        return await self.__get_transactions_by_account_id(account_id)

    async def read(self, id: int) -> Record:
        return await self.__get_by_id(id)

    async def __get_transactions_by_account_id(self, account_id: int) -> list[Record]:
        query = transactions.select().where(transactions.c.account_id == account_id)
        accounts = await database.fetch_all(query)

        if not accounts:
            raise NotFoundAccountError
        return accounts

    async def __get_by_id(self, id: int) -> Record:
        query = transactions.select().where(transactions.c.id == id)
        transaction = database.fetch_one(query)
        if not transaction:
            raise NotFoundTransactionError
        return transaction

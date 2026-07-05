import inspect

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from dio_bank.config import settings

settings.database_url = 'sqlite:///tests.db'


@pytest_asyncio.fixture
async def db(request):
    from dio_bank.database import database, engine, metadata  # noqa

    await database.connect()
    metadata.create_all(engine)

    yield database

    try:
        await database.disconnect()
        metadata.drop_all(engine)
    finally:
        # Força o fechamento de todas as conexões pendentes no pool
        if hasattr(engine, "dispose"):
            if inspect.iscoroutinefunction(engine.dispose):
                await engine.dispose()
            else:
                engine.dispose()


@pytest_asyncio.fixture
async def populate_db(db):
    from dio_bank.schemas.account import AccountIn  # noqa
    from dio_bank.schemas.transaction import TransactionIn  # noqa
    from dio_bank.services.account import AccountService  # noqa
    from dio_bank.services.transaction import TransactionService  # noqa

    transaction_service = TransactionService()
    account_service = AccountService()

    await account_service.create(AccountIn(holder='Joaquin', balance=235.77))
    await account_service.create(
        AccountIn(holder='Amelie', balance=5000000000)
        )
    await account_service.create(AccountIn(holder='Vhirishn', balance=2))
    await transaction_service.make_transaction(
        TransactionIn(amount=35.77, transaction='withdraw'), 1
        )
    await transaction_service.make_transaction(
        TransactionIn(amount=500, transaction='deposit'), 1
        )
    await transaction_service.make_transaction(
        TransactionIn(amount=3000, transaction='deposit'), 3
        )


@pytest_asyncio.fixture
async def client(db, populate_db):
    from dio_bank.app import app # noqa

    transport = ASGITransport(app=app)
    headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json'
    }
    async with AsyncClient(base_url='http://test',
                           transport=transport,
                           headers=headers) as client:
        yield client


@pytest_asyncio.fixture
async def access_token(client: AsyncClient):
    response = await client.post('/auth/login', json={'user_id': 1})

    return response.json()['access_token']

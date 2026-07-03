import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from dio_bank.database import database
from dio_bank.config import settings
from dio_bank.views.account import AccountOut
from dio_bank.models.account import accounts

settings.database_url = 'sqlite:///tests.db'


@pytest_asyncio.fixture
async def db(request):
    from dio_bank.database import database, engine, metadata

    await database.connect()
    metadata.create_all(engine)

    yield database

    await database.disconnect()
    metadata.drop_all(engine)


@pytest_asyncio.fixture
async def client(db):
    from dio_bank.app import app

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


@pytest_asyncio.fixture
async def dummy_account(db) -> AccountOut:
    command = accounts.insert().values(
        holder='aman',
        balance=777
    )

    record_id = await database.execute(command)
    query = accounts.select().where(accounts.c.id == record_id)

    return await database.fetch_one(query)

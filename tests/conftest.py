import asyncio

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from dio_bank.config import settings

settings.database_url = 'sqlite:///tests.db'


@pytest_asyncio.fixture
async def db(request):
    from dio_bank.database import database, engine, metadata

    await database.connect()
    metadata.create_all(engine)

    def teardown():
        async def _teardown():
            await database.disconnect()
            metadata.drop_all()

        asyncio.run(_teardown())

    request.add_finalizer(teardown)


@pytest_asyncio.fixture
async def client(db):
    from dio_bank.app import app

    transport = ASGITransport(app=app)
    headers = {
        'Accept': 'aplication/json',
        'Content-type': 'aplication/json'
    }

    async with AsyncClient(base_url='http://test',
                           transport=transport,
                           headers=headers) as client:
        yield client


async def access_token(client: AsyncClient):
    response = await client.post('/auth/login', json={'user_id': 1})

    return response.json()['access_token']

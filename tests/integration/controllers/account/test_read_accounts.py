from fastapi import status
from httpx import AsyncClient


async def test_read_accounts_success(
        client: AsyncClient, access_token: str
    ):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await client.get('/accounts/', headers=headers)

    assert len(response.json()) == 3  # noqa
    assert response.json()[0]['holder'] == 'Joaquin'


async def test_read_accounts_with_limit(
        client: AsyncClient, access_token: str
    ):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = await client.get(
        '/accounts/', params={'limit': 2}, headers=headers
    )

    assert len(response.json()) == 2  # noqa
    assert response.json()[1]['holder'] == 'Amelie'


async def test_fail_read_accounts_unauthorized(client: AsyncClient):
    response = await client.get('/accounts/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid authorization code.'}

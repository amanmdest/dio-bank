from fastapi import status
from httpx import AsyncClient


async def test_read_all(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get('/transactions/', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3  # noqa


async def test_read_all_limit(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get(
        '/transactions/',
        headers=headers,
        params={'limit': 1}
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 1  # noqa


async def test_fail_read_all_unauthorized(client: AsyncClient):
    response = await client.get('/transactions/')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid authorization code.'}

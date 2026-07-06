from fastapi import status
from httpx import AsyncClient


async def test_create_account_success(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'holder': 'Lucado', 'balance': 180}

    response = await client.post('/accounts/', json=data, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['id'] == 4  # noqa
    assert response.json()['holder'] == 'Lucado'


async def test_fail_create_account_missing_field(
    client: AsyncClient, access_token: str
):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'holder': 'Lucado'}

    response = await client.post('/accounts/', json=data, headers=headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT
    assert response.json()['detail'][0]['loc'] == ['body', 'balance']


async def test_fail_create_account_unauthorized(client: AsyncClient):
    data = {'holder': 'Lucado', 'balance': 1800}

    response = await client.post('/accounts/', json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

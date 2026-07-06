from fastapi import status
from httpx import AsyncClient


async def test_update_account(client: AsyncClient, access_token: str):
    account_id = 2
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'holder': 'Phoenix', 'balance': 777}

    response = await client.put(
        f'accounts/{account_id}', json=data, headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == 2  # noqa
    assert response.json()['balance'] == 777.0  # noqa


async def test_fail_update_account_not_found(
    client: AsyncClient, access_token: str
):
    account_id = 22
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'holder': 'Phoenix', 'balance': 777}

    response = await client.put(
        f'accounts/{account_id}', json=data, headers=headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account Not Found.'}


async def test_fail_update_account_unauthorized(client: AsyncClient):
    account_id = 2
    data = {'holder': 'Phoenix', 'balance': 777}

    response = await client.put(f'accounts/{account_id}', json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid authorization code.'}

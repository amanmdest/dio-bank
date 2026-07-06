from fastapi import status
from httpx import AsyncClient


async def test_read_account_by_id_success(
    client: AsyncClient, access_token: str
):
    headers = {'Authorization': f'Bearer {access_token}'}
    account_id = 3
    response = await client.get(f'/accounts/{account_id}', headers=headers)

    assert response.json()['holder'] == 'Vhirishn'


async def test_fail_read_account_by_id_unauthorized(client: AsyncClient):
    account_id = 3
    response = await client.get(f'/accounts/{account_id}')

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid authorization code.'}

from fastapi import status
from httpx import AsyncClient


async def test_create_account_success(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'holder': 'Lucado', 'balance': 180}

    response = await client.post('/accounts/', json=data, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['id'] == 4
    assert response.json()['holder'] == 'Lucado'



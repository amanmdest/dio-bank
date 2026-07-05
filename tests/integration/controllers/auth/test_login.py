from fastapi import status
from httpx import AsyncClient


async def test_login(client: AsyncClient):
    data = {'user_id': 1}
    response = await client.post('/auth/login', json=data)

    assert response.status_code == status.HTTP_200_OK
    assert 'access_token' in response.json()

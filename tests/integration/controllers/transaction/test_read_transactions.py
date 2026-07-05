from httpx import AsyncClient

from fastapi import status


async def test_read_all(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get('/transactions/', headers=headers)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 3

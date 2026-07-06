from fastapi import status
from httpx import AsyncClient


async def test_delete_account_success(client: AsyncClient, access_token: str):
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.delete(f'/accounts/{1}', headers=headers)
    response_read_all = await client.get('/accounts/', headers=headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert len(response_read_all.json()) == 2  # noqa


async def test_fail_delete_account_not_found(
    client: AsyncClient, access_token: str
):
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.delete(f'/accounts/{6}', headers=headers)
    response_read_all = await client.get('/accounts/', headers=headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account Not Found.'}
    assert len(response_read_all.json()) == 3  # noqa


async def test_fail_delete_account_unauthorized(
    client: AsyncClient, access_token: str
):
    response = await client.delete(f'/accounts/{1}')
    response_read_all = await client.get(
        '/accounts/', headers={'Authorization': f'Bearer {access_token}'}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert len(response_read_all.json()) == 3  # noqa

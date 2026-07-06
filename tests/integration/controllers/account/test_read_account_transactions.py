from fastapi import status
from httpx import AsyncClient


async def test_read_transaction_by_account_id_success(
    client: AsyncClient, access_token: str
):
    account_id = 1
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get(
        f'/accounts/{account_id}/transactions', headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 2  # noqa


async def test_read_transaction_by_account_id_not_found(
    client: AsyncClient, access_token: str
):
    account_id = 88
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get(
        f'/accounts/{account_id}/transactions', headers=headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account Not Found.'}

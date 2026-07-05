from fastapi import status
from httpx import AsyncClient


async def test_read_transaction_by_id_success(
        client: AsyncClient,
        access_token: str
    ):
    transaction_id = 1
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get(
        f'/transactions/{transaction_id}',
        headers=headers
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == 1  # noqa
    assert response.json()['amount'] == 35.77  # noqa
    assert response.json()['transaction'] == 'withdraw'


async def test_fail_read_transaction_by_id_not_found(
        client: AsyncClient,
        access_token: str
    ):
    transaction_id = 12
    headers = {'Authorization': f'Bearer {access_token}'}

    response = await client.get(
        f'/transactions/{transaction_id}',
        headers=headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Transaction Not Found.'}

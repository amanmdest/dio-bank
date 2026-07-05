from fastapi import status
from httpx import AsyncClient


async def test_make_deposit_transaction(
        client: AsyncClient,
        access_token: str
    ):
    headers = {'Authorization': f'Bearer {access_token}'}
    account_id = 1
    data = {'transaction': 'deposit', 'amount': 1500}
    response = await client.post(
        f'/transactions/{account_id}', json=data, headers=headers
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['transaction'] == 'deposit'
    assert response.json()['amount'] == 1500.0  # noqa


async def test_fail_make_deposit_transaction_account_not_found(
        client: AsyncClient,
        access_token: str
    ):
    headers = {'Authorization': f'Bearer {access_token}'}
    account_id = 11
    data = {'transaction': 'deposit', 'amount': 1500}
    response = await client.post(
        f'/transactions/{account_id}',
        json=data,
        headers=headers
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Account Not Found.'}


async def test_fail_make_deposit_transaction_uauthorized(client: AsyncClient):
    account_id = 1
    data = {'transaction': 'deposit', 'amount': 1500}
    response = await client.post(f'/transactions/{account_id}', json=data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'detail': 'Invalid authorization code.'}

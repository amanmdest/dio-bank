from fastapi import status
from httpx import AsyncClient


async def test_make_deposit_transaction(client: AsyncClient, access_token: str, dummy_account):
    headers = {'Authorization': f'Bearer {access_token}'}
    data = {'transaction': 'deposit', 'amount': 1500}

    response = await client.post(f'/transactions/{dummy_account.id}', json=data, headers=headers)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()['transaction'] == 'deposit'
    assert response.json()['amount'] == 1500.0

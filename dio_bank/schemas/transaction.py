from pydantic import BaseModel

from dio_bank.models.transaction import TransactionType


class TransactionIn(BaseModel):
    account_id: int
    transaction: TransactionType
    amount: float

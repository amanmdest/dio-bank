from pydantic import BaseModel

from dio_bank.models.transaction import TransactionType


class TransactionIn(BaseModel):
    transaction: TransactionType
    amount: float

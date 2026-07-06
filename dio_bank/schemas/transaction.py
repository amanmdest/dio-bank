from pydantic import BaseModel, PositiveFloat

from dio_bank.models.transaction import TransactionType


class TransactionIn(BaseModel):
    transaction: TransactionType
    amount: PositiveFloat

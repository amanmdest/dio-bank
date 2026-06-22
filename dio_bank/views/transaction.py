from pydantic import AwareDatetime, BaseModel

from dio_bank.models.transaction import TransactionType


class TransactionOut(BaseModel):
    id: int
    account_id: int
    transaction: TransactionType
    amount: float
    created_at: AwareDatetime

    class Config:
        from_attributes = True

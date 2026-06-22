from pydantic import BaseModel


class AccountIn(BaseModel):
    holder: str
    balance: float


class AccountPut(BaseModel):
    holder: str | None = None
    balance: float | None = None

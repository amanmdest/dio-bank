from pydantic import AwareDatetime, BaseModel


class AccountSchema(BaseModel):
    id: int
    holder: str
    balance: float
    transfer: float
    created_at: AwareDatetime | None = None
    updated_at: AwareDatetime | None = None


class AccountPut(BaseModel):
    holder: str | None = None
    balance: float | None = None
    transfer: float | None = None
    updated_at: AwareDatetime | None = None

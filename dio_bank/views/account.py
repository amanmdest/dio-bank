from pydantic import AwareDatetime, BaseModel


class AccountOut(BaseModel):
    id: int
    holder: str
    balance: float
    created_at: AwareDatetime

    class Config:
        from_attributes = True

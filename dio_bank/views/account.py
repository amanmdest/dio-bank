from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator


class AccountOut(BaseModel):
    id: int
    holder: str
    balance: float
    created_at: datetime

    @field_validator('created_at', mode='before')
    @classmethod
    def assegurar_timezone(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            return v.replace(tzinfo=timezone.utc)
        return v

    model_config = ConfigDict(from_attributes=True)

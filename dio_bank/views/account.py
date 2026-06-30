from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator

# class AccountOut(BaseModel):
#     id: int
#     holder: str
#     balance: float
#     created_at: AwareDatetime

#     class Config:
#         from_attributes = True


class AccountOut(BaseModel):
    id: int
    holder: str
    balance: float
    created_at: datetime  # Mudamos para datetime padrão

    # Usamos um validador para garantir que ele sempre saia com timezone
    @field_validator('created_at', mode='before')
    @classmethod
    def assegurar_timezone(cls, v):
        if isinstance(v, datetime) and v.tzinfo is None:
            # Se vier sem fuso horário do banco, assume UTC
            return v.replace(tzinfo=timezone.utc)
        return v

    # Configuração correta para Pydantic V2
    model_config = ConfigDict(from_attributes=True)

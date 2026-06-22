from fastapi import APIRouter

from dio_bank.schemas.auth import LoginIn
from dio_bank.security import sign_jwt
from dio_bank.views.auth import LoginOut

router = APIRouter(prefix='/auth')


@router.post('/login', response_model=LoginOut)
async def login(data: LoginIn):
    return sign_jwt(user_id=data.user_id)

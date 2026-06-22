from fastapi import APIRouter, Depends

from dio_bank.security import login_required

router = APIRouter(
    prefix='/transactions', dependencies=[Depends(login_required)]
)

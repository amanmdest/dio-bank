from fastapi import APIRouter, Depends

from dio_bank.security import login_required

router = APIRouter(prefix='/accounts', dependencies=[Depends(login_required)])


router.post('/')
def create_account(): ...
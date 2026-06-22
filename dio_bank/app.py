from contextlib import asynccontextmanager

from fastapi import FastAPI

from dio_bank.controllers import auth, account
from dio_bank.database import database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(title='DIO Bank API', lifespan=lifespan)
app.include_router(account.router, tags='accounts')
app.include_router(auth.router, tags=['auth'])


@app.get('/')
async def read_root():
    return {'message': 'no céu tem pão?'}

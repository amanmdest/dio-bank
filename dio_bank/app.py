from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from dio_bank.controllers import account, auth, transaction
from dio_bank.database import database
from dio_bank.exceptions import NotFoundAccountError, NotFoundTransactionError


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


tags_metadata = [
    {'name': 'auth', 'description': 'Authenticate to operate!'},
    {
        'name': 'accounts',
        'description': 'Bank accounts registries - \
            a holder can have more than one account, so far',
    },
    {
        'name': 'transactions',
        'description': 'Accounts transactions, incomes,\
            outcomes and history.',
        'externalDocs': {
            'description': 'Transactions.api external documentation.',
            'url': 'https://Posts.api.tiangolo.com/',
        },
    },
]


app = FastAPI(
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    summary="Dio's Favorite Bank, Pucci said",
    title='DIO Bank API',
    version='1.0.0',
)

app.include_router(account.router, tags=['accounts'])
app.include_router(auth.router, tags=['auth'])
app.include_router(transaction.router, tags=['transactions'])


@app.exception_handler(NotFoundAccountError)
async def not_found_account_exception_handler(
    request: Request, exc: NotFoundAccountError
):
    return JSONResponse(
        status_code=exc.status_code, content={'detail': exc.message}
    )


@app.exception_handler(NotFoundTransactionError)
async def not_found_transaction_exception_handler(
    request: Request, exc: NotFoundTransactionError
):
    return JSONResponse(
        status_code=exc.status_code, content={'detail': exc.message}
    )

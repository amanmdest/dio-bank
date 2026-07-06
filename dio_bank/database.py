import databases
import sqlalchemy as sa

from dio_bank.config import settings

DATABASE_URL = settings.database_url

metadata = sa.MetaData()
database = databases.Database(DATABASE_URL)

engine = sa.create_engine(
    DATABASE_URL, connect_args={'check_same_thread': False}
)

from dio_bank.models.account import accounts  # noqa
from dio_bank.models.transaction import transactions  # noqa

metadata.create_all(engine)

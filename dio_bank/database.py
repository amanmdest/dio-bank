import databases
import sqlalchemy as sa

from dio_bank.config import settings

DATABASE_URL = settings.database_url

metadata = sa.MetaData()
database = databases.Database(DATABASE_URL)

engine = sa.create_engine(DATABASE_URL)

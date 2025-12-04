from os import getenv
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

load_dotenv()

POSTGRES_USER = getenv("POSTGRES_USER")
POSTGRES_PASSWORD = getenv("POSTGRES_PASSWORD")
POSTGRES_DB = getenv("POSTGRES_DB")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DB_HOST}:{DB_PORT}/{POSTGRES_DB}"

engine = create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine)

# Создание сессии
async def get_session():
    async with new_session() as session:
        yield session


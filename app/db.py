import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import DATABASE_URL

DATABASE_URL = DATABASE_URL
ASYNC_PG_DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

pool: asyncpg.Pool | None = None

async def execute_sql(sql: str) -> int:
    """
    Выполняет SQL и возвращает одно число.
    Безопасность: только SELECT.
    """
    sql_lower = sql.strip().lower()
    if not sql_lower.startswith("select"):
        raise ValueError("Неверный запрос")

    async with pool.acquire() as conn:
        result = await conn.fetchval(sql)
        return result or 0

async def on_startup():
    """ Создаёт пул соединений с БД """
    global pool
    pool = await asyncpg.create_pool(ASYNC_PG_DATABASE_URL)
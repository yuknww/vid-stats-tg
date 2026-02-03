import asyncio
import asyncpg

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

DATABASE_URL = DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def create_pool():
    return await asyncpg.create_pool(DATABASE_URL)

pool = asyncio.run(create_pool())

async def execute_sql(sql: str) -> int:
    """
    Выполняет SQL и возвращает одно число.
    Безопасность: только SELECT.
    """
    sql_lower = sql.strip().lower()
    if not sql_lower.startswith("select"):
        raise ValueError("Только SELECT разрешён!")

    async with pool.acquire() as conn:
        result = await conn.fetchval(sql)
        return result or 0
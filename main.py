import asyncio
import logging

from app.config import dp, bot
from app.handlers import router
from app.load_data import load_json_to_db
from app.db import on_startup

logging.basicConfig(level=logging.INFO)
dp.include_router(router)

async def main():
    """ При запуске создаёт пул соединений, загружает данные в БД и запускает бота """

    try:
        await on_startup()
        await load_json_to_db()
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
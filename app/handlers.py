from aiogram.filters import Command
from aiogram.types import Message

from api import llm_generate_sql
from db import execute_sql
from main import dp

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот аналитики видео. Напишите Ваш вопрос.")

@dp.message()
async def handler(message: Message):
    user_question = message.text

    sql = await llm_generate_sql(user_question)

    try:
        answer = await execute_sql(sql)
    except Exception as e:
        answer = f"Ошибка выполнения SQL: {e}"

    await message.answer(str(answer))


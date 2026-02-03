from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.api import llm_generate_sql
from app.db import execute_sql

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привет! Я бот аналитики видео. Напишите Ваш вопрос.")

@router.message()
async def handler(message: Message):
    """ Слушает все текстовые сообщения и обрабатывает запрос """
    user_question = message.text

    sql = await llm_generate_sql(user_question)

    try:
        answer = await execute_sql(sql)
    except Exception as e:
        answer = f"Ошибка выполнения SQL: {e}"

    await message.answer(str(answer))


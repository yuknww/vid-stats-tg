import logging
import re

from groq import AsyncGroq

from app.config import API_KEY, SYSTEM_PROMPT

logger = logging.getLogger()
client = AsyncGroq(api_key=API_KEY)


def clean_sql(llm_output: str) -> str:
    """
    Убирает ```sql ... ``` и лишний текст
    """
    text = llm_output.strip()

    if text.startswith("```"):
        text = re.sub(r"^```[\w]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)

    return text.strip()

async def llm_generate_sql(question: str) -> str:
    """
    Отправляет запрос в LLM и возвращает чистый SQL
    :param question: вопрос пользователя
    :return: sql код
    """

    completion = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0
    )
    raw = completion.choices[0].message.content.strip()
    logger.info(f"Ответ от ИИ: {raw}")
    return clean_sql(raw)
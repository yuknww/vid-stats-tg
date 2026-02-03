from groq import AsyncGroq

from config import API_KEY, SYSTEM_PROMPT

client = AsyncGroq(api_key=API_KEY)


async def llm_generate_sql(question: str) -> str:
    completion = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0
    )
    return completion.choices[0].message.content.strip()
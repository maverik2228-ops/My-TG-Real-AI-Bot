import os
import asyncio
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

# Берем токены из переменных окружения Railway
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = "llama-3.3-70b-versatile"
API_URL = "https://api.groq.com/openai/v1/chat/completions"

bot = Bot(token=TELEGRAM_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()

def query_groq(text):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": text}]
    }
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=30)
        return response.json()["choices"][0]["message"]["content"]
    except:
        return "Ошибка связи с ИИ."

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Бот успешно переехал на Railway и работает 24/7!")

@dp.message()
async def handle(message: types.Message):
    res = await asyncio.to_thread(query_groq, message.text)
    await message.answer(res)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
import httpx
import asyncio
from dotenv import load_dotenv
from aiogram import F

load_dotenv()

TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://travel-rag-app:8001/answer"

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    downloaded = await bot.download_file(file.file_path)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            files = {'file': ('image.jpg', downloaded, 'image/jpeg')}
            resp = await client.post(f"{API_URL.replace('/answer', '/answer-image')}", files=files)
            data = resp.json()
            await message.answer(str(data["answer"]), parse_mode=ParseMode.HTML)
        except Exception as e:
            await message.answer(f"Error: {str(e)}")

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
    """*Hey there, traveler\\!*

I'm your personal travel assistant\\. Ask me about destinations, visas, safety, hotels, food \\- anything travel\\-related\\!

*Quick examples:*
"Best time to visit Italy?"
"Visa requirements for Dubai"
"Cheap eats in Bangkok"

Ready to explore? Just ask away\\! 🌍✈️
""",
    parse_mode=ParseMode.MARKDOWN_V2
)
@dp.message()
async def handle_query(message: types.Message):
    print("="*25 + message.text + "="*25 )
    async with httpx.AsyncClient(timeout=60.0) as client:  # увеличь timeout
        try:
            resp = await client.post(API_URL, json={"text": message.text}) 
            data = resp.json()
            print(data["answer"])
            await message.answer(
                str(data["answer"]),
                parse_mode=ParseMode.HTML,
                )
        except httpx.ReadTimeout:
            print('TimeOut')
            await message.answer("API request timeout")
        except Exception as e:
            print('Exception')
            await message.answer(f"Error: {str(e)}")

async def main():
    print("🤖 Bot starting...")
    # Сбрасываем старые webhook и очищаем очередь апдейтов
    await bot.delete_webhook(drop_pending_updates=True)
    # Стартуем polling, пропуская старые апдейты
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())

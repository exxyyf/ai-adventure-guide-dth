import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
import httpx
import asyncio
from dotenv import load_dotenv
from aiogram import F
import re

load_dotenv()

TOKEN=os.getenv("TELEGRAM_BOT_TOKEN")
API_URL = "http://travel-rag-app:8001/answer"

bot = Bot(token=TOKEN)
dp = Dispatcher()


async def send_long_message(message: types.Message, text: str, chunk_size: int = 4096):
    """Отправляет длинное сообщение частями, сохраняя целостность HTML-тегов"""
    if len(text) <= chunk_size:
        await message.answer(text, parse_mode=ParseMode.HTML)
        return
    
    chunks = []
    current_pos = 0
    
    while current_pos < len(text):
        # Берем chunk
        end_pos = min(current_pos + chunk_size, len(text))
        chunk = text[current_pos:end_pos]
        
        # Ищем незакрытые теги
        open_tags = re.findall(r'<(b|i|u|code|pre|a[^>]*)>', chunk)
        close_tags = re.findall(r'</(b|i|u|code|pre|a)>', chunk)
        
        # Считаем открытые теги (без пары)
        tag_stack = []
        for tag in open_tags:
            tag_name = tag.split()[0]  # для <a href...> берем только 'a'
            tag_stack.append(tag_name)
        for tag in close_tags:
            if tag_stack and tag_stack[-1] == tag:
                tag_stack.pop()
        
        # Если есть незакрытые теги, откатываемся до последнего полного тега
        if tag_stack and end_pos < len(text):
            # Ищем последний закрывающий тег в chunk
            last_close = max([chunk.rfind(f'</{t}>') for t in ['b', 'i', 'u', 'code', 'pre', 'a']] + [-1])
            if last_close > 0:
                end_pos = current_pos + last_close + len('</x>')
                chunk = text[current_pos:end_pos]
        
        chunks.append(chunk)
        current_pos = end_pos
    
    # Отправляем chunks
    for chunk in chunks:
        await message.answer(chunk, parse_mode=ParseMode.HTML)
        await asyncio.sleep(0.05)


@dp.message(F.photo)
async def handle_photo(message: types.Message):
    photo = message.photo[-1]
    file = await bot.get_file(photo.file_id)
    downloaded = await bot.download_file(file.file_path)
    
    # Получаем текст, если есть
    caption = message.caption or ""
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            files = {'file': ('image.jpg', downloaded, 'image/jpeg')}
            data_payload = {'caption': caption}
            resp = await client.post(f"{API_URL.replace('/answer', '/answer-image')}", files=files, data=data_payload)
            data = resp.json()
            await send_long_message(message, str(data["answer"]))
        except Exception as e:
            await message.answer(f"Error: {str(e)}")

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
    """<b>Hey there, traveler!</b>

I'm your personal travel assistant. Ask me about destinations, visas, food - anything travel-related!

<b>Quick examples:</b>
"Best time to visit Italy?"
"Visa requirements for Dubai"
"Cheap eats in Bangkok"

Ready to explore? Just ask away! 🌍✈️
""",
    parse_mode=ParseMode.HTML
)
@dp.message()
async def handle_query(message: types.Message):
    print("="*25 + message.text + "="*25 )
    async with httpx.AsyncClient(timeout=60.0) as client:  # увеличь timeout
        try:
            resp = await client.post(API_URL, json={"text": message.text}) 
            data = resp.json()
            print(data["answer"])
            await send_long_message(message, str(data["answer"]))
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

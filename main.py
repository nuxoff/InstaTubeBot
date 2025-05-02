import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import ParseMode
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я InstaTubeBot. Отправь мне ссылку на видео из YouTube или Instagram, и я скачаю его для тебя.")

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        await message.reply("Пожалуйста, пришли ссылку на видео.")
        return

    await message.reply("Скачиваю видео, подожди немного...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best',
        'quiet': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as video:
            await message.reply_video(video)
        os.remove(filename)
    except Exception as e:
        await message.reply("Не удалось скачать видео. Убедись, что ссылка правильная.")
        print(e)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

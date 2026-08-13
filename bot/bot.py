import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "SIZNING_BOT_TOKEN")
# Diqqat: Telegram Mini App faqat HTTPS manzilda ishlaydi.
# Lokal test uchun ngrok yoki Vercel/Railway kabi xizmatga deploy qiling.
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://your-domain.example/webapp")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📚 KitobJavon — ochish",
                    web_app=WebAppInfo(url=WEBAPP_URL),
                )
            ]
        ]
    )
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "<b>KitobJavon</b> botiga xush kelibsiz.\n"
        "Bu yerda siz:\n"
        "📖 Kitob sotishingiz\n"
        "🔄 Kitob almashtirishingiz\n"
        "📅 Kitob ijaraga berishingiz mumkin\n\n"
        "Boshlash uchun quyidagi tugmani bosing 👇",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

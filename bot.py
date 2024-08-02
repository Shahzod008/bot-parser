import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from handlers import register_commands
from buttons import main_keyboard

logging.basicConfig(level=logging.INFO)
bot = Bot(token="7368529760:AAFxoadDq5v1qI8l42GD280JA-7EUlWkaHo")
dp = Dispatcher()


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Выберите команду.", reply_markup=main_keyboard)


@dp.message(Command('start_parsing'))
async def start_parsing_command(message: types.Message):
    await message.answer("Парсинг запущен.")


async def main():
    await register_commands(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

import os

from telethon import TelegramClient, events
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from asyncio import Lock, create_task, run
from models import Channel, session, Keyword
from handlers import register_commands
import asyncio
import signal
import sys

lock = Lock()

# Инициализация Telethon клиента (как пользователь)
api_id = 27055341
api_hash = '70cda85a5eba41237cc9e3d47b3098c0'
client = TelegramClient('user', api_id, api_hash, system_version='4.16.30-vxCUSTOM')

# Инициализация Aiogram бота (как бот)
bot_token = "7240894789:AAHoGPHpVQ-wlgoDP4MU9SLly2jvuADhmYI"
bot = Bot(token=bot_token)
dp = Dispatcher()

target_channel_id = -4286804779  # ID целевого канала для отправки сообщений


async def forward_message_to_channel(message_text, user_name):
    try:
        await bot.send_message(
            chat_id=target_channel_id,
            text=f"{message_text}\n\nОт: @{user_name}",
            parse_mode='Markdown'
        )
        print(f"Сообщение успешно отправлено в канал {target_channel_id}.")
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


async def fetch_channels():
    channels = session.query(Channel.channel).all()
    channels = [ch[0] for ch in channels]
    print(f"Каналы для чтения: {channels}")
    return channels


async def fetch_keywords():
    keywords = session.query(Keyword.keyword).all()
    keywords = [kw[0] for kw in keywords]
    print(f"Ключевые слова: {keywords}")
    return keywords


async def restart_bot():
    print("Перезапуск бота...")
    await dp.stop_polling()
    await bot.session.close()
    await client.disconnect()
    # Перезапуск скрипта
    python = sys.executable
    os.execl(python, python, *sys.argv)


async def main():
    print("Программа запущена.")
    channels = await fetch_channels()
    keywords = await fetch_keywords()

    @client.on(events.NewMessage(chats=channels))
    async def handler(event):
        print("Новое сообщение получено.")
        message_text = event.message.message
        sender = await event.get_sender()
        user_name = sender.username if sender else "неизвестный пользователь"

        print(f"Сообщение от @{user_name}: {message_text}")

        async with lock:
            if any(keyword.lower() in message_text.lower() for keyword in keywords):
                print(f"Сообщение содержит ключевое слово: {message_text}")
                await forward_message_to_channel(message_text, user_name)
            else:
                print("Ключевые слова не найдены в сообщении.")

    # Регистрация команд aiogram
    @dp.message(Command(commands=["start"]))
    async def send_welcome(message: types.Message):
        await message.answer("Привет! Я бот, который отслеживает ключевые слова в каналах и пересылает сообщения.")

    @dp.message(Command(commands=["restart"]))
    async def restart_command(message: types.Message):
        await message.answer("Перезапуск бота...")
        create_task(restart_bot())

    await register_commands(dp)
    print("Команды зарегистрированы.")

    # Запуск бота aiogram в отдельной задаче
    create_task(dp.start_polling(bot))
    print("Бот aiogram запущен.")

    async with client:
        print("Клиент Telethon запущен.")
        await client.run_until_disconnected()
    print("Клиент Telegram отключен.")


if __name__ == '__main__':
    run(main())
    print("Программа завершена.")

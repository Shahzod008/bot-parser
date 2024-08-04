from aiogram.filters import Command
from telethon import TelegramClient, events
from aiogram import Bot, Dispatcher, types
from models import Channel, session, Keyword, MinusWord, Spammer, Message
from handlers import register_commands
from buttons import main_keyboard
import logging
import asyncio
from config import api_id, api_hash, system_version, token

logging.basicConfig(level=logging.INFO)

lock = asyncio.Lock()

client = TelegramClient(
    session='user',
    api_hash=api_hash,
    api_id=api_id,
    system_version=system_version
)

bot = Bot(token=token)
dp = Dispatcher()
channels = []
keywords = []
minus_words = []
spammers = []


@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Выберите команду.", reply_markup=main_keyboard)


async def update_channels_and_keywords():
    global channels, keywords, minus_words, spammers
    while True:
        try:
            channels = [ch[0] for ch in session.query(Channel.channel).all()]
            keywords = [kw[0] for kw in session.query(Keyword.keyword).all()]
            minus_words = [mw[0] for mw in session.query(MinusWord.minus_word).all()]
            spammers = [sp[0] for sp in session.query(Spammer.spammer).all()]
            print(channels, keywords, minus_words, spammers)

            client.remove_event_handler(handler, events.NewMessage)
            client.add_event_handler(handler, events.NewMessage(chats=channels))

            await asyncio.sleep(0.1)
        except Exception as e:
            logging.error(f"Ошибка при обновлении данных: {e}")


@client.on(events.NewMessage(chats=channels))
async def handler(event):
    try:
        async with lock:
            message_text = event.message.message
            user_name = event.sender.username

            if message_text:
                if not message_text.strip():
                    return

                if user_name is None:
                    user_name = "неизвестный пользователь"

                if user_name in spammers:
                    return

                if any(minus_word.lower() in message_text.lower() for minus_word in minus_words):
                    return

                if any(keyword.lower() in message_text.lower() for keyword in keywords):

                    existing_message = session.query(Message).filter_by(content=message_text).first()
                    if existing_message:
                        return

                    new_message = Message(content=message_text, username=user_name, channel=event.chat_id)
                    session.add(new_message)
                    session.commit()

                    text = f"{message_text}\n\nОт: @{user_name}"
                    chat_id = -4256836605
                    await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logging.error(f"Ошибка в обработке сообщения: {e}")


async def main():
    await register_commands(dp)
    asyncio.create_task(update_channels_and_keywords())
    asyncio.create_task(dp.start_polling(bot))

    async with client:
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
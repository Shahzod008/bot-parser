import logging
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from models import session, Keyword, MinusWord, Chat, Channel, Spammer


async def add_items(message: Message, model_class, item_type: str):
    command, _, text = message.text.partition(f" ")

    logging.info(f"Received text for adding {item_type}: {text}")

    if not text:
        await message.answer(f"Пожалуйста, укажите {item_type.replace('_', ' ')} для добавления.")
        return

    items = [item.strip() for item in text.split(',')]

    added_items = []
    existing_items = []

    for item in items:
        if item:
            existing_item = session.query(model_class).filter_by(**{item_type: item}).first()
            if existing_item:
                existing_items.append(item)
            else:
                new_item = model_class(**{item_type: item})
                session.add(new_item)
                added_items.append(item)

    session.commit()

    response = ""
    if added_items:
        response += f"Добавлены {item_type.replace('_', ' ')}: {', '.join(added_items)}.\n"
    if existing_items:
        response += f"{item_type.replace('_', ' ')} уже существуют: {', '.join(existing_items)}."

    if not response:
        response = f"Не добавлено ни одного {item_type.replace('_', ' ')}."

    await message.answer(response)


async def remove_items(message: Message, model_class, item_type: str):
    command, _, text = message.text.partition(f" ")

    if not text:
        await message.answer(f"Пожалуйста, укажите {item_type.replace('_', ' ')} для удаления.")
        return

    items = [item.strip() for item in text.split(',')]

    removed_items = []
    not_found_items = []

    for item in items:
        if item:
            existing_item = session.query(model_class).filter_by(**{item_type: item}).first()
            if existing_item:
                session.delete(existing_item)
                removed_items.append(item)
            else:
                not_found_items.append(item)

    session.commit()

    response = ""
    if removed_items:
        response += f"Удалены {item_type.replace('_', ' ')}: {', '.join(removed_items)}.\n"
    if not_found_items:
        response += f"{item_type.replace('_', ' ')} не найдены: {', '.join(not_found_items)}. Проверьте, пожалуйста."

    if not response:
        response = f"Не удалено ни одного {item_type.replace('_', ' ')}."

    await message.answer(response)


async def process_command(message: Message, model, action):
    if action.startswith('add_'):
        attribute_name = action.split('add_')[1]
        await add_items(message, model, attribute_name)
    elif action.startswith('remove_'):
        attribute_name = action.split('remove_')[1]
        await remove_items(message, model, attribute_name)


async def register_command(dp: Dispatcher, action, model):
    @dp.message(Command(action))
    async def command_handler(message: Message):
        await process_command(message, model, action)


async def register_commands(dp: Dispatcher):
    commands = [
        ('add_keyword', Keyword),
        ('remove_keyword', Keyword),
        ('add_minus_word', MinusWord),
        ('remove_minus_word', MinusWord),
        ('add_spammer', Spammer),
        ('remove_spammer', Spammer),
        ('add_channel', Channel),
        ('remove_channel', Channel),
        ('add_chat', Chat),
        ('remove_chat', Chat),
    ]

    for action, model in commands:
        await register_command(dp, action, model)

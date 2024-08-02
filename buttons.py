from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb = [
    [KeyboardButton(text="/add_keyword"), KeyboardButton(text="/remove_keyword")],
    [KeyboardButton(text="/add_minus_word"), KeyboardButton(text="/remove_minus_word")],
    [KeyboardButton(text="/add_spammer"), KeyboardButton(text="/remove_spammer")],
    [KeyboardButton(text="/add_channel"), KeyboardButton(text="/remove_channel")],
    [KeyboardButton(text="/add_chat"), KeyboardButton(text="/remove_chat")],
    [KeyboardButton(text="/start_parsing")],
]

main_keyboard = ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
    input_field_placeholder="Выберите команду"
)

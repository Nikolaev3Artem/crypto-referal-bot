from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_account = KeyboardButton("account")
button_help = KeyboardButton("help")

command_keyboard = ReplyKeyboardMarkup().add(button_account, button_help)

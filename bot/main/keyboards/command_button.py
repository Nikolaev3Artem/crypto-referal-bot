from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup

button_account = InlineKeyboardButton("account", callback_data="account")
button_help = InlineKeyboardButton("help", callback_data="help")

command_keyboard = ReplyKeyboardMarkup().add(button_account, button_help)

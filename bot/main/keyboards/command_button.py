from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_account = InlineKeyboardButton("account", callback_data="account")
button_help = InlineKeyboardButton("help", callback_data="help")

command_keyboard = InlineKeyboardMarkup().add(button_account, button_help)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.main.constants.enums import StartMenuEnum

button_account = InlineKeyboardButton("account", callback_data=StartMenuEnum.ACCOUNT)
button_help = InlineKeyboardButton("help", callback_data=StartMenuEnum.HELP)

command_keyboard = InlineKeyboardMarkup().add(button_account, button_help)

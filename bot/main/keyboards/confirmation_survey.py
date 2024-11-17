from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

accept = InlineKeyboardButton("Да", callback_data="yes")
decline = InlineKeyboardButton("Нет", callback_data="no")

user_confirmation_keyboard = InlineKeyboardMarkup().add(accept, decline)

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from backend.constants.enums import BlockchainEnum

start_keyboard = InlineKeyboardMarkup(resize_keyboard=True)

for coin in BlockchainEnum:
    start_keyboard.insert(InlineKeyboardButton(coin, callback_data=coin))

start_keyboard.add(InlineKeyboardButton("Больше адрессов нет", callback_data="FinishSurvey"))

accept = InlineKeyboardButton("Да", callback_data="yes")
decline = InlineKeyboardButton("Нет", callback_data="no")

user_confirmation_keyboard = InlineKeyboardMarkup().add(accept, decline)

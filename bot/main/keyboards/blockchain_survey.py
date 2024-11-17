from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

accept = InlineKeyboardButton("Да", callback_data="yes")
decline = InlineKeyboardButton("Нет", callback_data="no")

button_ethereum = InlineKeyboardButton("Ethereum", callback_data="Ethereum")
button_base = InlineKeyboardButton("Base", callback_data="Base")
button_polygon = InlineKeyboardButton("Polygon", callback_data="Polygon")
button_solana = InlineKeyboardButton("Solana", callback_data="Solana")
button_bsc = InlineKeyboardButton("BSC", callback_data="BSC")
button_tron = InlineKeyboardButton("Tron", callback_data="Tron")

start_keyboard = InlineKeyboardMarkup(row_width=3).add(
    button_bsc, button_base, button_ethereum, button_polygon, button_solana, button_tron
)


user_confirmation_keyboard = InlineKeyboardMarkup().add(accept, decline)

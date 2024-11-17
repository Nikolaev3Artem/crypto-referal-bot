from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

button_ethereum = KeyboardButton("Ethereum", callback_data="Ethereum")
button_base = KeyboardButton("Base", callback_data="Base")
button_polygon = KeyboardButton("Polygon", callback_data="Polygon")
button_solana = KeyboardButton("Solana", callback_data="Solana")
button_bsc = KeyboardButton("BSC", callback_data="BSC")
button_tron = KeyboardButton("Tron", callback_data="Tron")

start_keyboard = ReplyKeyboardMarkup(row_width=3).add(
    button_bsc, button_base, button_ethereum, button_polygon, button_solana, button_tron
)

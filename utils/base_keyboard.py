from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_ethereum = InlineKeyboardButton("Ethereum", callback_data="Ethereum")
button_base = InlineKeyboardButton("Base", callback_data="Base")
button_polygon = InlineKeyboardButton("Polygon", callback_data="Polygon")
button_solana = InlineKeyboardButton("Solana", callback_data="Solana")
button_bsc = InlineKeyboardButton("BSC", callback_data="BSC")
button_tron = InlineKeyboardButton("Tron", callback_data="Tron")

start_keyboard = InlineKeyboardMarkup(row_width=2).add(
    button_bsc, button_base, button_ethereum, button_polygon, button_solana, button_tron
)

button_yes = InlineKeyboardButton("Да", callback_data="yes")
button_no = InlineKeyboardButton("Нет", callback_data="no")

choice_yes_no_keyboard = InlineKeyboardMarkup().add(button_yes, button_no)

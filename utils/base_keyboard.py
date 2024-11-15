from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

button_ethereum = InlineKeyboardButton("Ethereum", callback_data="ethereum")
button_base = InlineKeyboardButton("Base", callback_data="base")
button_polygon = InlineKeyboardButton("Polygon", callback_data="polygon")
button_solana = InlineKeyboardButton("Solana", callback_data="solana")
button_bsc = InlineKeyboardButton("BSC", callback_data="bsc")
button_tron = InlineKeyboardButton("Tron", callback_data="tron")

start_keyboard = InlineKeyboardMarkup(row_width=2).add(
    button_bsc, button_base, button_ethereum, button_polygon, button_solana, button_tron
)

button_yes = InlineKeyboardButton("Да", callback_data="yes")
button_no = InlineKeyboardButton("Нет", callback_data="no")

user_choice_keyboard = InlineKeyboardMarkup().add(button_yes, button_no)

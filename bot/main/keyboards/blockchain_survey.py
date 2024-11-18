from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from backend.constants.enums import BlockchainEnum

button_ethereum = InlineKeyboardButton("Ethereum", callback_data=BlockchainEnum.ETHEREUM)
button_base = InlineKeyboardButton("Base", callback_data=BlockchainEnum.BASE)
button_polygon = InlineKeyboardButton("Polygon", callback_data=BlockchainEnum.POLYGON)
button_solana = InlineKeyboardButton("Solana", callback_data=BlockchainEnum.SOLANA)
button_bsc = InlineKeyboardButton("BSC", callback_data=BlockchainEnum.BSC)
button_tron = InlineKeyboardButton("Tron", callback_data=BlockchainEnum.TRON)

start_keyboard = InlineKeyboardMarkup(row_width=3).add(
    button_bsc, button_base, button_ethereum, button_polygon, button_solana, button_tron
)


accept = InlineKeyboardButton("Да", callback_data="yes")
decline = InlineKeyboardButton("Нет", callback_data="no")

user_confirmation_keyboard = InlineKeyboardMarkup().add(accept, decline)

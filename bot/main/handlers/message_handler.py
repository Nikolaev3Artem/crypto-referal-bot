from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.main.handlers.base_command_handlers import send_acc_info, send_help
from bot.main.handlers.blockchain_handler import (
    request_handler_base,
    request_handler_bsc,
    request_handler_ethereum,
    request_handler_polygon,
    request_handler_solana,
    request_handler_tron,
)
from bot.main.loader import dp


@dp.message_handler()
async def handle_message(message: types.Message, state: FSMContext):
    if message.text == "account":
        await send_acc_info(message)
    if message.text == "help":
        await send_help(message)
    if message.text == "Ethereum":
        await state.update_data(message=message.text)
        await request_handler_ethereum(message, state)
    if message.text == "Base":
        await state.update_data(message=message.text)
        await request_handler_base(message, state)
    if message.text == "Polygon":
        await state.update_data(message=message.text)
        await request_handler_polygon(message, state)
    if message.text == "Solana":
        await state.update_data(message=message.text)
        await request_handler_solana(message, state)
    if message.text == "BSC":
        await state.update_data(message=message.text)
        await request_handler_bsc(message, state)
    if message.text == "Tron":
        await state.update_data(message=message.text)
        await request_handler_tron(message, state)

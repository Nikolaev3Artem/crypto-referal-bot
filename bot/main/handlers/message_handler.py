from aiogram import types

from bot.main.bot_instance import dp
from bot.main.handlers.base_command_handlers import send_acc_info, send_help


@dp.message_handler()
async def handle_message(message: types.Message):
    if message.text == "account":
        await send_acc_info(message)
    if message.text == "help":
        await send_help(message)

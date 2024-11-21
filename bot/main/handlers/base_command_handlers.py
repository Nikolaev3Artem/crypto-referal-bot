from aiogram import types

from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.constants.enums import StartMenuEnum
from bot.main.handlers.blockchain_handler import user_state
from bot.main.keyboards.blockchain_survey import start_keyboard
from bot.repositories.messages_repo import message_repository


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    inviter_id = None

    if len(message.text.split()) > 1:
        try:
            inviter_id = int(message.text.split()[1])
        except ValueError:
            inviter_id = None

    if inviter_id:
        if user_id not in user_state:
            user_state[user_id] = {}
        user_state[user_id]["invited_by"] = inviter_id

    start_message = await message_repository.get_start_message()
    await message.answer(start_message.message, reply_markup=start_keyboard)


@dp.callback_query_handler(lambda c: c.data == StartMenuEnum.ACCOUNT)
async def send_acc_info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    account_message = await message_repository.get_account_message()
    context = {
        "refferal_link": await UserService.get_refferal_link(user_id=user_id),
        "refferals_count": await UserService.get_user_refferals_count(user_id=user_id),
        "user_points": await UserService.get_user_points(user_id=user_id),
    }
    formatted_message = account_message.message.format(**context)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, formatted_message)


@dp.callback_query_handler(lambda c: c.data == StartMenuEnum.HELP)
async def send_help(callback_query: types.CallbackQuery):
    help_message = await message_repository.get_help_message()
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, help_message.message)

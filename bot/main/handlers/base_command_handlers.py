from aiogram import types

from backend.repositories.user_repo import user_repository
from backend.schemas.user import UserCreate
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.constants.enums import StartMenuEnum
from bot.main.keyboards.blockchain_survey import start_keyboard
from bot.repositories.messages_repo import message_repository


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    try:
        await user_repository.get_user(message["from"]["id"])
    except Exception:
        user = message["from"]
        user = UserCreate(
            user_id=user["id"],
            username=user["username"] if "username" in user else None,
            language=user["language_code"] if "language_code" in user else None,
        )
        await user_repository.create_user(user)

        if len(message.text) > 7 and str(message["from"]["id"]) != message.text[7:]:
            invited_by = message.text[7:]
            await user_repository.update_invited_by(message["from"]["id"], invited_by=invited_by)
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

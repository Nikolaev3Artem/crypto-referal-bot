from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.constants.enums import BlockchainEnum
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.keyboards.command_button import command_keyboard
from bot.main.keyboards.blockchain_survey import start_keyboard
from core.settings import settings
from bot.repositories.messages_repo import message_repository

user_state = {}


@dp.callback_query_handler(lambda c: c.data in [blockchain.value for blockchain in BlockchainEnum])
async def select_blockchain(callback_query: types.CallbackQuery):
    user_state[callback_query.from_user.id] = {"blockchain": callback_query.data}

    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")

@dp.callback_query_handler(lambda c: c.data == "FinishSurvey")
async def handle_callback_button_end(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query['from']['id']
    addresses = await UserService.check_user_addresses_exists(user_id=user_id)
    refferal_link = f"https://t.me/{settings.BOT_NICKNAME}?start={user_id}"
    survey_completed = await message_repository.get_survey_completed_message()
    no_addresses_message = await message_repository.get_no_addresses_message()

    if not addresses:
        await bot.send_message(
            callback_query.from_user.id,
            no_addresses_message.message,
            reply_markup=start_keyboard,
        )
        return

    await UserService.update_refferral_link_link(
        user_id=callback_query["from"]["id"],
        refferral_link=refferal_link,
    )
    context = {
        "refferal_link": refferal_link,
    }
    formatted_message = survey_completed.message.format(**context)

    await bot.send_message(
        callback_query.from_user.id,
        formatted_message,
        reply_markup=command_keyboard,
    )
    await state.finish()

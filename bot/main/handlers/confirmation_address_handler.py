from aiogram import types

from bot.main.bot_instance import bot, dp
from bot.main.handlers.blockchain_handler import HANDLERS, user_state
from bot.main.keyboards.blockchain_survey import start_keyboard, user_confirmation_keyboard
from bot.main.states import BlockchainSurvey


@dp.callback_query_handler(lambda c: c.data in ["yes", "no"], state=BlockchainSurvey.confirmation)
async def confirm_address(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if callback_query.data == "yes":
        blockchain = user_state[user_id]["blockchain"]
        address = user_state[user_id]["address"]

        handler = HANDLERS[blockchain]
        await handler(address, blockchain, user_id)
    else:
        user_state.pop(user_id)
        await bot.send_message(
            callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
        )


@dp.message_handler(
    lambda message: message.from_user.id in user_state and "blockchain" in user_state[message.from_user.id],
    state=BlockchainSurvey.address,
)
async def process_confirm_address(message: types.Message):
    user_id = message.from_user.id
    user_state[user_id]["address"] = message.text

    await message.reply(f"Подтверджаете адрес {message.text}?", reply_markup=user_confirmation_keyboard)
    await BlockchainSurvey.confirmation.set()

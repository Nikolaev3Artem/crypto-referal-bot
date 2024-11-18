from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.main.bot_instance import bot, dp
from bot.main.keyboards.blockchain_survey import start_keyboard, user_confirmation_keyboard
from bot.main.keyboards.command_button import command_keyboard
from bot.main.states import BlockchainSurvey


@dp.callback_query_handler(lambda c: c.data in ["yes", "no"], state=BlockchainSurvey.confirmation)
async def process_handler_button_yes_no(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        # user_data = await state.get_data()
        # address = user_data.get("address", None)
        # blockchain = user_data.get("blockchain", None)
        # #для валидации определенного адреса и блокчейна
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id,
            """Спасибо! Свяжемся когда ваши активы заинтересуют нас.\n
Вот твоя реферальная ссылка (ссылка)\n
Делись с друзьями, за это ты будешь получать Олегобаллы, которые ты сможкешь использовать для...""",
            reply_markup=command_keyboard,
        )
        await state.finish()
    elif callback_query.data == "no":
        await bot.send_message(
            callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
        )
        await state.finish()


@dp.message_handler(state=BlockchainSurvey.address)
async def process_confirm_address(message: types.Message, state: FSMContext):
    address = message.text
    await state.update_data(address=address)
    await message.answer("Подтверждаете адрес?", reply_markup=user_confirmation_keyboard)

    await BlockchainSurvey.confirmation.set()

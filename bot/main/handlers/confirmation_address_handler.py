from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.repositories.blockchain_repo import blockchain_repository
from backend.repositories.user_repo import user_repository
from backend.schemas.address import AddressCreate
from backend.services.blockchain_service import BlockchainService
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.keyboards.blockchain_survey import start_keyboard, user_confirmation_keyboard
from bot.main.states import BlockchainSurvey
from core.settings import settings


@dp.callback_query_handler(lambda c: c.data in ["yes", "no", "FinishSurvey"], state=BlockchainSurvey.confirmation)
async def process_handler_button_yes_no(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        user_data = await state.get_data()
        address = user_data.get("address")
        blockchain = user_data.get("blockchain")
        user_id = callback_query["from"]["id"]
        address_exist = await blockchain_repository.address_exists_check(address=address)
        if address_exist is not None:
            await bot.send_message(
                callback_query.from_user.id,
                "Этот адресс уже используется, пожалуйста введите другой",
                reply_markup=start_keyboard,
            )
            await state.finish()

        address = AddressCreate(
            address=address,
            owner_id=user_id,
            blockchain=blockchain,
        )
        address = await BlockchainService.create_address(address)
        await UserService.reward_on_connection(user_id=user_id)
        referrer_first = await user_repository.refferer_user_exist_first_level(user_id=user_id)
        if referrer_first is not None:
            await UserService.reward_first_level(user_id=user_id)
        # перевірка на валідність tron
        # validation_address = await BlockchainService.validate_tron_address(address=address)
        # if validation_address['status'] == 404:
        #     await bot.send_message(
        #         callback_query.from_user.id, validation_address['result'], reply_markup=start_keyboard
        #     )
        #     await state.finish()

        # if validation_address['status'] == 200:
        #     await bot.answer_callback_query(callback_query.id)
        #     await bot.send_message(
        #         callback_query.from_user.id, f"Отлично, адресс сохранен \n Вы получили {user_points}",
        #  reply_markup=start_keyboard
        #     )
        #     await state.finish()
        await UserService.update_refferral_link_link(
            user_id=user_id, refferral_link=f"https://t.me/{settings.BOT_NICKNAME}?start={callback_query['from']['id']}"
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
    await message.answer(f"Подтверждаете адрес {address}?", reply_markup=user_confirmation_keyboard)

    await BlockchainSurvey.confirmation.set()

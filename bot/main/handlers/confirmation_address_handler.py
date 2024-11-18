from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.schemas.address import AddressCreate

# from backend.schemas.user import UserBase
from backend.services.blockchain_service import BlockchainService
from backend.repositories.blockchain_repo import blockchain_repository

from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.keyboards.blockchain_survey import start_keyboard, user_confirmation_keyboard
from bot.main.keyboards.command_button import command_keyboard
from bot.main.states import BlockchainSurvey


@dp.callback_query_handler(lambda c: c.data in ["yes", "no", "FinishSurvey"], state=BlockchainSurvey.confirmation)
async def process_handler_button_yes_no(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "yes":
        user_data = await state.get_data()
        address = user_data.get("address")
        blockchain = user_data.get("blockchain")
        # print(callback_query["from"]["id"])
        # try:
        #     await blockchain_repository.get_address()
        # except Exception:
        # user = await user_repository.get_user(callback_query["from"]["id"])
        # owner = UserBase(
        #     user_id=callback_query["from"]["id"],

        # )
        address_exist = await blockchain_repository.address_exists_check(address=address)
        if address_exist is not None:
            await bot.send_message(
                callback_query.from_user.id, "Этот адресс уже используется, пожалуйста введите другой", reply_markup=start_keyboard
            )
            await state.finish()
        
        address = AddressCreate(
            address=address,
            owner_id=callback_query["from"]["id"],
            blockchain=blockchain,
        )
        address = await BlockchainService.create_address(address)
        
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(
            callback_query.from_user.id, "Отлично, адресс сохранен", reply_markup=start_keyboard
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
from aiogram import types

from backend.constants.enums import BlockchainEnum
from backend.repositories.blockchain_repo import blockchain_repository
from backend.repositories.user_repo import user_repository
from backend.schemas.address import AddressCreate
from backend.services.blockchain_service import BlockchainService
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.handlers.blockchain_handler import user_state
from bot.main.keyboards.blockchain_survey import start_keyboard, user_confirmation_keyboard

HANDLERS = {
    BlockchainEnum.ETHEREUM: BlockchainService.validate_etereum_address,
    BlockchainEnum.BASE: BlockchainService.validate_base_address,
    BlockchainEnum.POLYGON: BlockchainService.validate_polygon_address,
    BlockchainEnum.SOLANA: BlockchainService.validate_solana_address,
    BlockchainEnum.BSC: BlockchainService.validate_bsc_address,
    BlockchainEnum.TRON: BlockchainService.validate_tron_address,
}

@dp.callback_query_handler(lambda c: c.data in ["yes", "no"])
async def confirm_address(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if callback_query.data == "yes":
        blockchain = user_state[user_id]["blockchain"]
        address = user_state[user_id]["address"]
        address_exist = await blockchain_repository.address_exists_check(address=address)
        if address_exist is not None:
            await bot.send_message(
                user_id,
                "Этот адресс уже используется, пожалуйста введите другой",
                reply_markup=start_keyboard,
            )
        else:
            handler = HANDLERS[blockchain]
            validation_address = await handler(address)

        if not validation_address:
            await bot.send_message(user_id, "Такого адреса не существует", reply_markup=start_keyboard)
        else:
            address = AddressCreate(
                address=address,
                owner_id=user_id,
                blockchain=blockchain,
            )
            await BlockchainService.create_address(address)
                # Выдача если это только первый адрес, можно сделать логику чтобы если у
                # пользователя это только первый ключ то була выдача баллов
            await UserService.reward_on_connection(user_id=user_id)
            if await user_repository.refferer_user_first_level(user_id=user_id) is not None:
                await UserService.reward_first_level(user_id=user_id)
            if await user_repository.refferer_user_second_level(user_id=user_id) is not None:
                await UserService.reward_second_level(user_id=user_id)

            await bot.send_message(
                user_id,
                "Отлично, адресс сохранен",
                reply_markup=start_keyboard,
            )

    else:
        user_state.pop(user_id)
        await bot.send_message(
            callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
        )


@dp.message_handler(
    lambda message: message.from_user.id in user_state and "blockchain" in user_state[message.from_user.id]
)
async def process_confirm_address(message: types.Message):
    user_id = message.from_user.id
    user_state[user_id]["address"] = message.text

    await message.reply(f"Подтверджаете адрес {message.text}?", reply_markup=user_confirmation_keyboard)

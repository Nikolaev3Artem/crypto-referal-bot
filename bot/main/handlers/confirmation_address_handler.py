from aiogram import types

from backend.constants.enums import BlockchainEnum
from backend.repositories.blockchain_repo import blockchain_repository
from backend.repositories.user_repo import user_repository
from backend.schemas.address import AddressCreate
from backend.schemas.user import UserCreate
from backend.services.blockchain_service import BlockchainService
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.handlers.blockchain_handler import user_state
from bot.main.keyboards.blockchain_survey import start_keyboard, user_confirmation_keyboard
from core.settings import settings

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
                "Этот адрес уже используется, пожалуйста введите другой",
                reply_markup=start_keyboard,
            )
            user_state.pop(user_id, None)
            return

        handler = HANDLERS[blockchain]
        validation_address = await handler(address)

        if not validation_address:
            await bot.send_message(user_id, "Такого адреса не существует", reply_markup=start_keyboard)
            user_state.pop(user_id, None)
            return

        if not await user_repository.user_exists_check(user_id=user_id):
            if user_id not in user_state:
                user_state[user_id] = {}

            user_create = UserCreate(
                user_id=user_id,
                username=callback_query.from_user.username if callback_query.from_user.username else None,
                language=callback_query.from_user.language_code if callback_query.from_user.language_code else None,
            )
            await user_repository.create_user(user_create)

            invited_by = user_state[user_id].get("invited_by")
            if invited_by:
                await user_repository.update_invited_by(callback_query["from"]["id"], invited_by=invited_by)
            await UserService.reward_on_connection(user_id=user_id)
            if await user_repository.refferer_user_first_level(user_id=user_id) is not None:
                await UserService.reward_first_level(user_id=user_id)
            if await user_repository.refferer_user_second_level(user_id=user_id) is not None:
                await UserService.reward_second_level(user_id=user_id)

            refferal_link = f"https://t.me/{settings.BOT_NICKNAME}?start={user_id}"
            await UserService.update_refferral_link_link(
                user_id=callback_query["from"]["id"],
                refferral_link=refferal_link,
            )

        address_create = AddressCreate(
            address=address,
            owner_id=user_id,
            blockchain=blockchain,
        )
        await BlockchainService.create_address(address_create)

        user_state.pop(user_id, None)

        await bot.send_message(
            user_id,
            "Отлично, адрес сохранен",
            reply_markup=start_keyboard,
        )

    else:
        user_state.pop(user_id, None)
        await bot.send_message(
            callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
        )


@dp.message_handler(
    lambda message: message.from_user.id in user_state and "blockchain" in user_state[message.from_user.id]
)
async def process_confirm_address(message: types.Message):
    user_id = message.from_user.id
    user_state[user_id]["address"] = message.text
    await message.reply(f"Подтверждаете адрес {message.text}?", reply_markup=user_confirmation_keyboard)

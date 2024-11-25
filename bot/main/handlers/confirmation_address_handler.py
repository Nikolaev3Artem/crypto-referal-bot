from aiogram import types

from backend.constants.enums import BlockchainEnum
from backend.repositories.blockchain_repo import blockchain_repository
from backend.repositories.user_repo import user_repository
from backend.schemas.address import AddressCreate
from backend.services.blockchain_service import BlockchainService
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp, logger
from bot.main.handlers.blockchain_handler import user_state
from bot.main.keyboards.blockchain_survey import start_keyboard, user_confirmation_keyboard
from bot.repositories.messages_repo import message_repository

HANDLERS = {
    BlockchainEnum.ETHEREUM: BlockchainService.validate_etereum_address,
    BlockchainEnum.SOLANA: BlockchainService.validate_solana_address,
    BlockchainEnum.TRON: BlockchainService.validate_tron_address,
}


@dp.callback_query_handler(lambda c: c.data in ["yes", "no"])
async def confirm_address(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    try:
        address_not_correct_message = await message_repository.get_address_not_correct_message()
        address_already_exists_message = await message_repository.get_address_already_exists_message()
        address_created_message = await message_repository.get_address_created_message()
    except Exception:
        logger.error("Не установлены необходимые переменные для сообщений бота, измените это в BotMessages")
    else:
        if callback_query.data == "yes":
            try:
                blockchain = user_state[user_id]["blockchain"]
                address = user_state[user_id]["address"]
            except KeyError as e:
                logger.info(f"Мы не ожидаем от пользователя {e} подтверждения адреса, так как id нет в user_state.")
            else:
                user_state.pop(user_id)

                address_exist = await blockchain_repository.address_exists_check(address=address)
                if address_exist is not None:
                    await bot.send_message(
                        user_id,
                        address_already_exists_message.message,
                        reply_markup=start_keyboard,
                    )
                    return
                else:
                    handler = HANDLERS[blockchain]
                    validation_address = await handler(address)

                if not validation_address:
                    await bot.send_message(user_id, address_not_correct_message.message, reply_markup=start_keyboard)
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
                        address_created_message.message,
                        reply_markup=start_keyboard,
                    )

        else:
            try:
                user_state.pop(user_id)
            except KeyError as e:
                logger.info(f"Мы не ожидаем от пользователя {e} подтверждения адреса, так как id нет в user_state.")
            else:
                await bot.send_message(
                    callback_query.from_user.id, address_not_correct_message.message, reply_markup=start_keyboard
                )


@dp.message_handler(
    lambda message: message.from_user.id in user_state and "blockchain" in user_state[message.from_user.id]
)
async def process_confirm_address(message: types.Message):
    try:
        user_id = message.from_user.id
        user_state[user_id]["address"] = message.text
    except KeyError as e:
        logger.info(f"Мы не ожидаем от пользователя {e} адреса, так как его id нет в user_state.")
    else:
        try:
            address_confirm_creating_message = await message_repository.get_address_confirm_creating_message()
        except Exception:
            logger.error("Не установлены необходимые переменные для сообщений бота, измените это в BotMessages")
        else:
            context = {
                "address": message.text,
            }
            formatted_message = address_confirm_creating_message.message.format(**context)

            await message.reply(formatted_message, reply_markup=user_confirmation_keyboard)

from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.constants.enums import BlockchainEnum
from backend.repositories.blockchain_repo import blockchain_repository
from backend.repositories.user_repo import user_repository
from backend.schemas.address import AddressCreate
from backend.services.blockchain_service import BlockchainService
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.keyboards.blockchain_survey import start_keyboard
from bot.main.keyboards.command_button import command_keyboard
from bot.main.states import BlockchainSurvey
from core.settings import settings

user_state = {}


@dp.callback_query_handler(lambda c: c.data in [blockchain.value for blockchain in BlockchainEnum])
async def select_blockchain(callback_query: types.CallbackQuery):
    user_state[callback_query.from_user.id] = {"blockchain": callback_query.data}

    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
    await BlockchainSurvey.address.set()


async def handle_tron(address: str, blockchain: str, user_id: int):
    address_exist = await blockchain_repository.address_exists_check(address=address)
    if address_exist is not None:
        await bot.send_message(
            user_id,
            "Этот адресс уже используется, пожалуйста введите другой",
            reply_markup=start_keyboard,
        )
    else:
        validation_address = await BlockchainService.validate_tron_address(address=address)
        if validation_address["status"] == 404:
            await bot.send_message(user_id, validation_address["result"], reply_markup=start_keyboard)

        if validation_address["status"] == 200:
            address = AddressCreate(
                address=address,
                owner_id=user_id,
                blockchain=blockchain,
            )
            await BlockchainService.create_address(address)

            await UserService.reward_on_connection(user_id=user_id)
            if await user_repository.refferer_user_first_level(user_id=user_id) is not None:
                await UserService.reward_first_level(user_id=user_id)
            if await user_repository.refferer_user_second_level(user_id=user_id) is not None:
                await UserService.reward_second_level(user_id=user_id)

            await bot.send_message(
                user_id,
                "Отлично, адресс сохранен \n Вы получили ",  # {user_points}",
                reply_markup=start_keyboard,
            )


async def handle_ethereum(address: str, blockchain: str, user_id: int):
    pass


async def handle_base(address: str, blockchain: str, user_id: int):
    pass


async def handle_polygon(address: str, blockchain: str, user_id: int):
    pass


async def handle_solana(address: str, blockchain: str, user_id: int):
    pass


async def handle_bsc(address: str, blockchain: str, user_id: int):
    pass


HANDLERS = {
    BlockchainEnum.ETHEREUM: handle_ethereum,
    BlockchainEnum.BASE: handle_base,
    BlockchainEnum.POLYGON: handle_polygon,
    BlockchainEnum.SOLANA: handle_solana,
    BlockchainEnum.BSC: handle_bsc,
    BlockchainEnum.TRON: handle_tron,
}


@dp.callback_query_handler(lambda c: c.data == "FinishSurvey")
async def handle_callback_button_end(callback_query: types.CallbackQuery, state: FSMContext):

    await UserService.update_refferral_link_link(
        user_id=callback_query["from"]["id"],
        refferral_link=f"https://t.me/{settings.BOT_NICKNAME}?start={callback_query['from']['id']}",
    )
    await bot.send_message(
        callback_query.from_user.id,
        """Спасибо! Свяжемся когда ваши активы заинтересуют нас.\n
Вот твоя реферальная ссылка (ссылка)\n
Делись с друзьями, за это ты будешь получать Олегобаллы, которые ты сможкешь использовать для...""",
        reply_markup=command_keyboard,
    )
    await state.finish()

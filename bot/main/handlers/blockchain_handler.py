from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.constants.enums import BlockchainEnum
from backend.services.blockchain_service import BlockchainService
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.keyboards.command_button import command_keyboard
from core.settings import settings

user_state = {}


@dp.callback_query_handler(lambda c: c.data in [blockchain.value for blockchain in BlockchainEnum])
async def select_blockchain(callback_query: types.CallbackQuery):
    user_state[callback_query.from_user.id] = {"blockchain": callback_query.data}

    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")


async def handle_tron(address: str):
    return await BlockchainService.validate_tron_address(address=address)


async def handle_ethereum(address: str):
    return await BlockchainService.validate_etereum_address(address=address)


async def handle_base(address: str):
    return await BlockchainService.validate_base_address(address=address)


async def handle_polygon(address: str):
    return await BlockchainService.validate_polygon_address(address=address)


async def handle_solana(address: str):
    return await BlockchainService.validate_solana_address(address=address)


async def handle_bsc(address: str):
    return await BlockchainService.validate_bsc_address(address=address)


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

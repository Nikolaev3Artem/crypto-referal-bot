from aiogram import types
from aiogram.dispatcher import FSMContext

from backend.constants.enums import BlockchainEnum
from bot.main.bot_instance import bot, dp
from bot.main.states import BlockchainSurvey
from bot.main.keyboards.command_button import command_keyboard


@dp.callback_query_handler(lambda c: c.data == BlockchainEnum.ETHEREUM)
async def handle_callback_button_ethereum(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(blockchain=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
    await BlockchainSurvey.address.set()


@dp.callback_query_handler(lambda c: c.data == BlockchainEnum.BASE)
async def handle_callback_button_base(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(blockchain=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
    await BlockchainSurvey.address.set()


@dp.callback_query_handler(lambda c: c.data == BlockchainEnum.POLYGON)
async def handle_callback_button_polygon(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(blockchain=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
    await BlockchainSurvey.address.set()


@dp.callback_query_handler(lambda c: c.data == BlockchainEnum.SOLANA)
async def handle_callback_button_solana(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(blockchain=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
    await BlockchainSurvey.address.set()


@dp.callback_query_handler(lambda c: c.data == BlockchainEnum.TRON)
async def handle_callback_button_tron(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(blockchain=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
    await BlockchainSurvey.address.set()


@dp.callback_query_handler(lambda c: c.data == BlockchainEnum.BSC)
async def handle_callback_button_bsc(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(blockchain=callback_query.data)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
    await BlockchainSurvey.address.set()

@dp.callback_query_handler(lambda c: c.data == "FinishSurvey")
async def handle_callback_button_bsc(callback_query: types.CallbackQuery, state: FSMContext):
        await bot.send_message(
            callback_query.from_user.id, 
            """Спасибо! Свяжемся когда ваши активы заинтересуют нас.\n
Вот твоя реферальная ссылка (ссылка)\n
Делись с друзьями, за это ты будешь получать Олегобаллы, которые ты сможкешь использовать для...""",
            reply_markup=command_keyboard,
        )
        await state.finish()
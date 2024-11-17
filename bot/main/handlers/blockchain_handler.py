from aiogram import types
from aiogram.dispatcher import FSMContext

from bot.main.loader import bot, dp
from bot.main.states import BlockchainSurvey


@dp.message_handler(commands=["Ethereum"])
async def request_handler_ethereum(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await bot.send_message(message.from_user.id, f"Введите ваш адрес для сети {message.text}")
    await BlockchainSurvey.address.set()


@dp.message_handler(commands=["Base"])
async def request_handler_base(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await bot.send_message(message.from_user.id, f"Введите ваш адрес для сети {message.text}")
    await BlockchainSurvey.address.set()


@dp.message_handler(commands=["Polygon"])
async def request_handler_polygon(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await bot.send_message(message.from_user.id, f"Введите ваш адрес для сети {message.text}")
    await BlockchainSurvey.address.set()


@dp.message_handler(commands=["Solana"])
async def request_handler_solana(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await bot.send_message(message.from_user.id, f"Введите ваш адрес для сети {message.text}")
    await BlockchainSurvey.address.set()


@dp.message_handler(commands=["BSC"])
async def request_handler_bsc(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await bot.send_message(message.from_user.id, f"Введите ваш адрес для сети {message.text}")
    await BlockchainSurvey.address.set()


@dp.message_handler(commands=["Tron"])
async def request_handler_tron(message: types.Message, state: FSMContext):
    await state.update_data(message=message.text)
    await bot.send_message(message.from_user.id, f"Введите ваш адрес для сети {message.text}")
    await BlockchainSurvey.address.set()

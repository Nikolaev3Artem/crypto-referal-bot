from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Импорт
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from django.core.management.base import BaseCommand

from core.settings import settings
from utils.base_keyboard import choice_yes_no_keyboard, start_keyboard

# Создаем класс для состояний


class Form(StatesGroup):
    waiting_for_address = State()  # Ожидаем ввод адреса


class Command(BaseCommand):
    help = "Launching the bot using the command"

    def handle(self, *args, **options):
        storage = MemoryStorage()  # Использ
        bot = Bot(token=settings.BOT_TOKEN)
        dp = Dispatcher(bot, storage=storage)

        @dp.message_handler(commands=["start"])
        async def send_welcome(message: types.Message):
            await message.answer(
                """
        Добро пожаловать на Olegobot, этот бот предназначен для дропов. Пожалуйста введите адрес своего кошелька,
        поставьте 0 если у вас нет его в этой сети, то нужно заполнить хотя бы 1 адрес.
                """,
                reply_markup=start_keyboard,
            )

        @dp.message_handler(commands=["account"])
        async def send_acc_info(message: types.Message):
            await message.reply(
                """
        Твои адреса:
        1. ETH/BASE/POLY:
        2. Solana
        3. BSC
        4. Tron

        Твоя рефка (ссылка)

        Рефералов: n

        Баллов: n Olegopoints
                """
            )

        @dp.message_handler(commands=["help"])
        async def send_help(message: types.Message):
            await message.reply(
                """
Всё очень просто. Вы заполняете ваши криптоадреса и получаете за это поинты.\n
Приглашаете своих друзей заполнить их данные - и ваши друзья получат х2 от
обычного количества поинтов за анкету, а вы получите бонус Y поинтов за каждого.\n
Зачем нужны поинты?\n
Представьте, что какой-то новый токен хочет обратить на себя внимание холдеров токена $brett.\n
Они обращаются к нам и говорят - мы готовы дать аирдропом 5% нашего токена всем активным холдерам $brett.\n
Мы проверяем этот новый токен на отсутствие скама (высокий налог на продажу, минтабл, 90% сапплая у команды и т.д.)\n
Если всё ок - мы выбираем из нашей базы анкет всех, кто держит сейчас 
$brett хотя бы на 5 долларов, и рассылаем им предложение получить аирдроп.\n
Всем, кто соглашается, мы присылаем аирдроп пропорционально их поинтам.\n
То есть, например, у нас есть 1.000.000 токенов на аирдроп и 100 человек согласилось его получить.\n
У них всех в сумме 20.000 поинтов - значит, мы раздадим токенов из расчёта 50 токенов за 1 
поинт. Если у вас 100 поинтов - получите 5000 токенов, если 200 - то получите 10000 токенов.\n\n
Поинты можно заработать не только заполнением анкет или приглашением друзей - следите за нашими рассылками в боте!\n
Иногда мы будем просто раздавать поинты в честь каких-либо событий (например,\t
10.000 пользователей или 25.000 пользователей бота - чем не повод всех порадовать)."""
            )

        @dp.callback_query_handler(lambda c: c.data == "yes")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            print(callback_query.data)
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Адрес записан")
            # Если неудача то даем ему кнопки для ввода
            await bot.send_message(
                callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
            )

        @dp.callback_query_handler(lambda c: c.data == "no")
        async def process_callback_button_no(callback_query: types.CallbackQuery):
            print(callback_query.data)
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
            )

        @dp.callback_query_handler()
        async def process_callback_button_yes(callback_query: types.CallbackQuery):
            print(callback_query.data)
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {callback_query.data}")
            # Переводим пользователя в состояние ожидания адреса
            await Form.waiting_for_address.set()

        @dp.message_handler(state=Form.waiting_for_address)
        async def process_address_input(message: types.Message, state: FSMContext):
            # Получаем введённое пользователем сообщение
            await message.answer("Подтверждаете адрес?", reply_markup=choice_yes_no_keyboard)

            # После того как адрес принят, завершаем состояние
            await state.finish()

        executor.start_polling(dp, skip_updates=True)

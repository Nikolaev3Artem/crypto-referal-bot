from aiogram import Bot, Dispatcher, executor, types
from django.core.management.base import BaseCommand

from core.settings import settings
from utils.base_keyboard import start_keyboard, user_choice_keyboard


class Command(BaseCommand):
    help = "Launching the bot using the command"

    def handle(self, *args, **options):

        bot = Bot(token=settings.BOT_TOKEN)
        dp = Dispatcher(bot)

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

        @dp.callback_query_handler(lambda c: c.data == "ethereum")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Введите ваш адрес для сети Ethereum")

        @dp.callback_query_handler(lambda c: c.data == "base")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Введите ваш адрес для сети Base")

        @dp.callback_query_handler(lambda c: c.data == "polygon")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Введите ваш адрес для сети Polygon")

        @dp.callback_query_handler(lambda c: c.data == "solana")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Введите ваш адрес для сети Solana")

        @dp.callback_query_handler(lambda c: c.data == "bsc")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Введите ваш адрес для сети BSC")

        @dp.callback_query_handler(lambda c: c.data == "tron")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Введите ваш адрес для сети Tron")

        @dp.message_handler()
        async def echo_user_input(message: types.Message):
            keyboard = user_choice_keyboard
            await message.answer("Подтверждаете адрес?", reply_markup=keyboard)
            dp.message_handlers.unregister(echo_user_input)

        @dp.callback_query_handler(lambda c: c.data == "yes")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, "Адрес записан")
            # Если неудача то даем ему кнопки для ввода
            await bot.send_message(
                callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
            )

        @dp.callback_query_handler(lambda c: c.data == "no")
        async def process_callback_button_ethereum(callback_query: types.CallbackQuery):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(
                callback_query.from_user.id, "Пожалуйста, введите верный адрес", reply_markup=start_keyboard
            )

        executor.start_polling(dp, skip_updates=True)
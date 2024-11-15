from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup
from django.core.management.base import BaseCommand

from core.settings import settings
from utils.base_keyboard import button_base, button_bsc, button_ethereum, button_polygon, button_solana, button_tron


class Command(BaseCommand):
    help = "Launching the bot using the command"

    def handle(self, *args, **options):

        bot = Bot(token=settings.BOT_TOKEN)
        dp = Dispatcher(bot)

        async def handle_button_click(callback_query: types.CallbackQuery, network_name: str):
            await bot.answer_callback_query(callback_query.id)
            await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {network_name}")

            @dp.message_handler(lambda message: message.from_user.id == callback_query.from_user.id)
            async def handle_user_message(message: types.Message):
                user_input = message.text
                await message.reply(f"Вы ввели: {user_input}")

                dp.message_handlers.unregister(handle_user_message)

        @dp.message_handler(commands=["start"])
        async def send_welcome(message: types.Message):

            keyboard = InlineKeyboardMarkup(row_width=2).add(
                button_bsc, button_base, button_ethereum, button_polygon, button_solana, button_tron
            )
            await message.answer(
                """
        Добро пожаловать на Olegobot, этот бот предназначен для дропов. Пожалуйста введите адрес своего кошелька,
        поставьте 0 если у вас нет его в этой сети, то нужно заполнить хотя бы 1 адрес.
                """,
                reply_markup=keyboard,
            )

        @dp.callback_query_handler(lambda c: c.data in ["ethereum", "base", "polygon", "solana", "bsc", "tron"])
        async def process_callback_button(callback_query: types.CallbackQuery):
            network_mapping = {
                "ethereum": "Ethereum",
                "base": "Base",
                "polygon": "Polygon",
                "solana": "Solana",
                "bsc": "BSC",
                "tron": "Tron",
            }

            network_name = network_mapping.get(callback_query.data)
            if network_name:
                await handle_button_click(callback_query, network_name)

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

        executor.start_polling(dp, skip_updates=True)

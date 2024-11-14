from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from core.settings import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


# Обрабатываем нажатие кнопки и ждем сообщение
async def handle_button_click(callback_query: types.CallbackQuery, network_name: str):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Введите ваш адрес для сети {network_name}")

    # Устанавливаем обработчик для следующего сообщения от пользователя
    @dp.message_handler(lambda message: message.from_user.id == callback_query.from_user.id)
    async def handle_user_message(message: types.Message):
        user_input = message.text  # Получаем введенное пользователем сообщение
        await message.reply(f"Вы ввели: {user_input}")  # Отправляем обратно сообщение

        # Убираем обработчик после получения сообщения
        dp.message_handlers.unregister(handle_user_message)


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    button_eth_etc = InlineKeyboardButton("Ethereum/Base/Polygon", callback_data="eth_etc")
    button_sol = InlineKeyboardButton("Solana", callback_data="solana")
    button_bsc = InlineKeyboardButton("BSC", callback_data="bsc")
    button_tron = InlineKeyboardButton("Tron", callback_data="tron")

    keyboard = InlineKeyboardMarkup(row_width=2).add(button_eth_etc, button_sol, button_bsc, button_tron)
    await message.answer(
        """
Добро пожаловать на Olegobot, этот бот предназначен для дропов. Пожалуйста введите адрес своего кошелька,
поставьте 0 если у вас нет его в этой сети, то нужно заполнить хотя бы 1 адрес.
        """,
        reply_markup=keyboard,
    )


# Обработчик нажатия на кнопки
@dp.callback_query_handler(lambda c: c.data in ["eth_etc", "solana", "bsc", "tron"])
async def process_callback_button(callback_query: types.CallbackQuery):
    network_mapping = {"eth_etc": "Ethereum/Base/Polygon", "solana": "Solana", "bsc": "BSC", "tron": "Tron"}

    network_name = network_mapping.get(callback_query.data)
    if network_name:
        await handle_button_click(callback_query, network_name)


# Обработчик команды /account
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


# Обработчик команды /help
@dp.message_handler(commands=["help"])
async def send_help(message: types.Message):
    await message.reply(
        """
Всё очень просто. Вы заполняете ваши криптоадреса и получаете за это поинты.                                 

Приглашаете своих друзей заполнить их данные - и ваши друзья получат х2 от обычногоколичества поинтов за анкету, а вы получите бонус Y поинтов за каждого.                                

Зачем нужны поинты?                                

Представьте, что какой-то новый токен хочет обратить на себя внимание холдеров токена $brett.                                 

Они обращаются к нам и говорят - мы готовы дать аирдропом 5% нашего токена всем активным холдерам $brett.                                

Мы проверяем этот новый токен на отсутствие скама (высокий налог на продажу, минтабл, 90% сапплая у команды и т.д.)                                

Если всё ок - мы выбираем из нашей базы анкет всех, кто держит сейчас $brett хотя бы на 5 долларов, и рассылаем им предложение получить аирдроп.                                

Всем, кто соглашается, мы присылаем аирдроп пропорционально их поинтам.                                

То есть, например, у нас есть 1.000.000 токенов на аирдроп и 100 человек согласилось его получить.                                

У них всех в сумме 20.000 поинтов - значит, мы раздадим токенов из расчёта 50 токенов за 1 поинт. Если у вас 100 поинтов - получите 5000 токенов, если 200 - то получите 10000 токенов.                                
                            

Поинты можно заработать не только заполнением анкет или приглашением друзей - следите за нашими рассылками в боте!                                 

Иногда мы будем просто раздавать поинты в честь каких-либо событий (например, 10.000 пользователей или 25.000 пользователей бота - чем не повод всех порадовать).
        """
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

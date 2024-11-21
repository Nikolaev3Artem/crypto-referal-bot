from aiogram import types

from backend.repositories.user_repo import user_repository
from backend.schemas.user import UserCreate
from backend.services.user_service import UserService
from bot.main.bot_instance import bot, dp
from bot.main.constants.enums import StartMenuEnum
from bot.main.keyboards.blockchain_survey import start_keyboard

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    try:
        await user_repository.get_user(message["from"]["id"])
    except Exception:
        if len(message.text) < 7 or str(message["from"]["id"]) == message.text[7:]:
            user = message["from"]
            user = UserCreate(
                user_id=user["id"],
                username=user["username"] if "username" in user else None,
                language=user["language_code"] if "language_code" in user else None,
            )
            await user_repository.create_user(user)
        else:
            invited_by = message.text[7:]
            user = message["from"]
            user = UserCreate(
                user_id=user["id"],
                username=user["username"] if "username" in user else None,
                language=user["language_code"] if "language_code" in user else None,
            )
            await user_repository.create_user(user)
            await user_repository.update_invited_by(message["from"]["id"], invited_by=invited_by)

    await message.answer(
        """
Добро пожаловать на Olegobot, этот бот предназначен для дропов. Пожалуйста введите адрес своего кошелька,
поставьте 0 если у вас нет его в этой сети, то нужно заполнить хотя бы 1 адрес.
        """,
        reply_markup=start_keyboard,
    )


@dp.callback_query_handler(lambda c: c.data == StartMenuEnum.ACCOUNT)
async def send_acc_info(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    refferal_link = await UserService.get_refferal_link(user_id=user_id)
    refferals_count = await UserService.get_user_refferals_count(user_id=user_id)
    user_points = await UserService.get_user_points(user_id=user_id)

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
        f"""

Твоя реферальная ссылка {refferal_link}

Рефералов: {refferals_count}

Баллов: {user_points} Olegopoints
        """,
    )


@dp.callback_query_handler(lambda c: c.data == StartMenuEnum.HELP)
async def send_help(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(
        callback_query.from_user.id,
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
10.000 пользователей или 25.000 пользователей бота - чем не повод всех порадовать).""",
    )

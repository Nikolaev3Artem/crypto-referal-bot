from aiogram import Bot, Dispatcher, executor, types
from core.settings import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(
        """Добро пожаловать на Olegobot, этот бот предназначен для дропов. Пожалуйста введите адрес своего кошелька,
        поставьте 0 если у вас нет его в этой сети, то нужно заполнить хотя бы 1 адрес."""
    )


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

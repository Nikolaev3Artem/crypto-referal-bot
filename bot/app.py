from aiogram import Bot, Dispatcher, executor, types
from core.settings import settings

bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
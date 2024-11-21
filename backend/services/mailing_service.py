import asyncio

from backend.repositories.mailings_repo import mailing_repository
from bot.main.bot_instance import bot


class MailingService:
    def __init__(self):
        self.bot = bot  # Используем импортированный экземпляр бота
        self.semaphore = asyncio.Semaphore(10)  # Ограничение до 10 одновременных задач

    async def send_mailing(self, mailing):
        """
        Отправляет сообщение всем пользователям, связанным с рассылкой.
        """
        try:
            # Получаем список user_id асинхронно через репозиторий
            user_ids = await mailing_repository.get_user_ids(mailing)

            # Создаём задачи для отправки сообщений
            tasks = [self.send_message(user_id, mailing.message) for user_id in user_ids]

            # Выполняем задачи параллельно с ограничением
            if tasks:
                await asyncio.gather(*tasks)

            # Помечаем рассылку как отправленную
            await mailing_repository.mark_as_sent(mailing)

            print(f"Рассылка {mailing.id} успешно отправлена.")
        except Exception as e:
            print(f"Ошибка при отправке рассылки {mailing.id}: {e}")
            raise  # Пробрасываем исключение вверх для обработки в admin.py

    async def send_message(self, chat_id, text):
        """
        Отправляет одно сообщение пользователю.
        """
        async with self.semaphore:
            try:
                await self.bot.send_message(chat_id=chat_id, text=text, parse_mode="HTML")
                print(f"Сообщение успешно отправлено пользователю {chat_id}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")

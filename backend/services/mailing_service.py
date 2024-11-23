import asyncio

from backend.repositories.mailings_repo import mailing_repository
from backend.services.user_service import UserService
from bot.main.bot_instance import bot


class MailingService:
    def __init__(self):
        self.bot = bot
        self.semaphore = asyncio.Semaphore(10)

    async def send_mailing(self, mailing):
        """
        Отправляет сообщение всем пользователям, связанным с рассылкой.
        """
        try:
            users = await mailing_repository.get_users(mailing)

            tasks = [self.send_message(user, mailing.message) for user in users]
            if tasks:
                await asyncio.gather(*tasks)

            await mailing_repository.mark_as_sent(mailing)

            print(f"Рассылка {mailing.id} успешно отправлена.")
        except Exception as e:
            print(f"Ошибка при отправке рассылки {mailing.id}: {e}")
            raise

    async def send_message(self, user, message_template):
        """
        Отправляет одно сообщение пользователю.
        """
        async with self.semaphore:
            try:
                refferal_link = await UserService.get_refferal_link(user_id=user.user_id)
                referrals_count = await UserService.get_user_refferals_count(user_id=user.user_id)
                user_points = await UserService.get_user_points(user_id=user.user_id)

                context = {
                    "refferal_link": refferal_link,
                    "referrals_count": referrals_count,
                    "user_points": user_points,
                    "username": user.username,
                }

                try:
                    formatted_message = message_template.format(**context)
                except KeyError as ke:
                    formatted_message = f"Error formatting message: missing key {ke}"
                    print(formatted_message)

                await self.bot.send_message(chat_id=user.user_id, text=formatted_message, parse_mode="HTML")
                print(f"Сообщение успешно отправлено пользователю {user.user_id}")
            except Exception as e:
                print(f"Ошибка при отправке сообщения пользователю {user.user_id}: {e}")

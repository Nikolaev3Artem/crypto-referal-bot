from asgiref.sync import sync_to_async

from backend.models import Mailings
from utils.base_repository import BaseRepository


class MailingRepository(BaseRepository):
    model = Mailings

    @sync_to_async
    def mark_as_sent(self, mailing: Mailings):
        """
        Помечает рассылку как отправленную.
        """
        mailing.send = True
        mailing.save()

    @sync_to_async
    def get_user_ids(self, mailing: Mailings):
        """
        Получает список user_id всех пользователей, связанных с рассылкой.
        """
        return list(mailing.users.values_list("user_id", flat=True))

    @sync_to_async
    def get_users(self, mailing: Mailings):
        """
        Возвращает список юзеров связаных с рассылкой
        """
        return list(mailing.users.all())


mailing_repository = MailingRepository(Mailings)

from asgiref.sync import sync_to_async

from backend.models import Mailings
from bot.models import BotMessages
from utils.base_repository import BaseRepository


class MessageRepository(BaseRepository):

    @sync_to_async
    def get_start_message(self) -> BotMessages:
        return BotMessages.objects.get(title="start_message")
    
    @sync_to_async
    def get_account_message(self) -> BotMessages:
        return BotMessages.objects.get(title="account_message")
    
    @sync_to_async
    def get_help_message(self) -> BotMessages:
        return BotMessages.objects.get(title="help_message")
    
    @sync_to_async
    def get_survey_completed_message(self) -> BotMessages:
        return BotMessages.objects.get(title="survey_completed_message")
    
    @sync_to_async
    def get_no_addresses_message(self) -> BotMessages:
        return BotMessages.objects.get(title="no_addresses_message")
    
    @sync_to_async
    def get_address_already_exists_message(self) -> BotMessages:
        return BotMessages.objects.get(title="address_already_exists_message")
    
    @sync_to_async
    def get_address_not_correct_message(self) -> BotMessages:
        return BotMessages.objects.get(title="address_not_correct_message")
    
    @sync_to_async
    def get_address_created_message(self) -> BotMessages:
        return BotMessages.objects.get(title="address_created_message")
    
    @sync_to_async
    def get_address_confirm_creating_message(self) -> BotMessages:
        return BotMessages.objects.get(title="address_confirm_creating_message")
    
message_repository = MessageRepository(BotMessages)

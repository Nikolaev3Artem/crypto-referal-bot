from aiogram import executor
from django.core.management.base import BaseCommand

from bot.main.handlers.confirmation_address_handler import process_handler_button_yes_no
from bot.main.handlers.message_handler import handle_message
from bot.main.loader import dp


class Command(BaseCommand):
    help = "Launching the bot using the command"

    def handle(self, *args, **options):

        dp.register_message_handler(handle_message)
        dp.register_callback_query_handler(process_handler_button_yes_no)

        executor.start_polling(dp, skip_updates=True)

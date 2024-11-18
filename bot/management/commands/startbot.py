# import os
# import sys

from aiogram import executor
from django.core.management.base import BaseCommand

from bot.main.bot_instance import dp
from bot.main.handlers.blockchain_handler import (
    handle_callback_button_base,
    handle_callback_button_bsc,
    handle_callback_button_ethereum,
    handle_callback_button_polygon,
    handle_callback_button_solana,
    handle_callback_button_tron,
)
from bot.main.handlers.confirmation_address_handler import process_handler_button_yes_no
from bot.main.handlers.message_handler import handle_message


class Command(BaseCommand):
    help = "Launching the bot using the command"

    # def restart_bot(self):
    #     os.execv(sys.executable, ["python"] + sys.argv)

    def handle(self, *args, **options):

        dp.register_message_handler(handle_message)
        dp.register_callback_query_handler(
            process_handler_button_yes_no,
            handle_callback_button_ethereum,
            handle_callback_button_base,
            handle_callback_button_polygon,
            handle_callback_button_solana,
            handle_callback_button_tron,
            handle_callback_button_bsc,
        )

        executor.start_polling(dp, skip_updates=True)
        # self.restart_bot()

# import os
# import sys

from aiogram import executor
from django.core.management.base import BaseCommand

from bot.main.bot_instance import dp
from bot.main.handlers.base_command_handlers import send_acc_info, send_help
from bot.main.handlers.blockchain_handler import handle_callback_button_end, select_blockchain
from bot.main.handlers.confirmation_address_handler import confirm_address, process_confirm_address


class Command(BaseCommand):
    help = "Launching the bot using the command"

    # def restart_bot(self):
    #     os.execv(sys.executable, ["python"] + sys.argv)

    def handle(self, *args, **options):

        dp.register_message_handler(process_confirm_address)
        dp.register_callback_query_handler(
            send_acc_info,
            send_help,
            confirm_address,
            select_blockchain,
            handle_callback_button_end,
        )

        executor.start_polling(dp, skip_updates=True)
        # self.restart_bot()

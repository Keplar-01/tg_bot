import logging
from os import getenv

from dotenv import load_dotenv
from telegram.ext import filters
from telegram import Update
from telegram.ext import Updater, CommandHandler, ApplicationBuilder, ContextTypes, CallbackQueryHandler, MessageHandler

from bot.services.CommandHandlerService import CommandHandlerService
load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def main():
    application = ApplicationBuilder().token(getenv("TG_TOKEN")).build()

    # start_handler = CommandHandler('start', RegistrationCommand.register)
    # add_to_wallet_handler = CommandHandler('add', ChangesWalletBalanceHandler.changes_wallet_balance)
    # extract_to_wallet_handler = CommandHandler('extract', ChangesWalletBalanceHandler.changes_wallet_balance)
    # watch_hitory_handler = CommandHandler('watch', WatchHistoryHandler.watch_history)
    # watch_balance_handler = CommandHandler('balance', WatchBalanceHandler.watch_balance)
    # delete_wallet_info_handler = CommandHandler('delete_info', DeleteWalletInfoHandler.delete_info)
    # delete_history_handler = CommandHandler('delete_history', DeleteHistoryHandler.delete_history)
    # create_custom_tax_handler = CommandHandler('create_custom_tax', CustomTaxHandler.create_custom_tax)
    #
    # application.add_handler(start_handler)
    # application.add_handler(add_to_wallet_handler)
    # application.add_handler(extract_to_wallet_handler)
    # application.add_handler(watch_hitory_handler)
    # application.add_handler(watch_balance_handler)
    # application.add_handler(delete_wallet_info_handler)
    # application.add_handler(delete_history_handler)
    # application.add_handler(create_custom_tax_handler)
    # application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, CustomTaxHandler.handle_custom_tax_click))

    command_handling_service = CommandHandlerService()
    application.add_handler(MessageHandler(filters.TEXT, command_handling_service.handle))
    application.add_handler(CallbackQueryHandler(command_handling_service.handle_callback_query))
    application.run_polling()


if __name__ == '__main__':
    main()

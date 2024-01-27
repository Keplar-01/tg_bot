from telegram import Update
from telegram.ext import CallbackContext

from bot.handlers.CommandInterface import CommandInterface
from bot.services.DatabaseService import DatabaseService
from database import Session
from utils.data_sources.SQLAlchemyDS import SQLAlchemyDataSource

database_service = DatabaseService(Session())


class RegistrationCommand(CommandInterface):
    __name_command__ = '/start'

    def get_name(self):
        return self.__name_command__

    async def execute(self, update: Update, context: CallbackContext):
        user_id = str(update.message.from_user.id)
        database_service.create_user(user_id)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Был успешно создан кошелек",
        )

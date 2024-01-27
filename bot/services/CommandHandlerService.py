from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from bot.handlers.RegistrationCommand import RegistrationCommand

registration_handler = RegistrationCommand()


class CommandHandlerService:
    def __init__(self):
        self.commands = [registration_handler]

    async def handle(self, update: Update, context: CallbackContext):
        text = update.message.text

        for command in self.commands:
            command_name = text.startswith(command.get_name())
            if command_name:
                await command.execute(update, context)
            else:
                keyboard = [
                    [InlineKeyboardButton("Список команд", callback_data='list_commands')],
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    reply_markup=reply_markup,
                    text=f"Неизвестная команда. Нажмите на кнопку 'Список комманд', чтобы получить полный список команд"
                )

    async def handle_callback_query(self, update: Update, context: CallbackContext):
        query = update.callback_query
        data = query.data

        if data == 'list_commands':
            command_list = "\n".join([command.get_name() for command in self.commands])
            await context.bot.send_message(
                chat_id=query.message.chat_id,
                text=f"Список команд:\n{command_list}")

# bot/handlers.py
import json

from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext

from bot.services.DatabaseService import DatabaseService
from database import Session

database_service = DatabaseService(Session())
class RegistrationHandler:
    @staticmethod
    async def register(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        database_service.create_user(user_id)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Был успешно создан кошелек",
        )


class ChangesWalletBalanceHandler:
    @staticmethod
    async def changes_wallet_balance(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        command, money, comment = update.message.text.split(' ', maxsplit=2)
        if command == '/add':
            money = abs(int(money))
        else:
            money = -abs(int(money))
        database_service.change_wallet_balance(str(user_id), money)
        database_service.update_history_balance(str(user_id),
                                                command,
                                                money,
                                                comment)
        balance = database_service.get_balance(str(user_id))

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Запись была учтена, текущий баланс: {balance}"
        )


class WatchHistoryHandler:
    @staticmethod
    async def watch_history(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        all_history = database_service.get_history_wallet(str(user_id))
        ans = ''
        for i in range(len(all_history)):
            ans += (f'{i}. {all_history[i].operation_type} - {all_history[i].amount} - '
                    f'{all_history[i].description}\n {all_history[i].timestamp}\n')
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"История изменений кошелька: \n{ans}"
        )


class WatchBalanceHandler:
    @staticmethod
    async def watch_balance(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"Текущий баланс: {database_service.get_balance(str(user_id))}"
        )


class DeleteWalletInfoHandler:
    @staticmethod
    async def delete_info(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        database_service.delete_user_info(str(user_id))

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Информация о пользователе удалена."
        )


class DeleteHistoryHandler:
    @staticmethod
    async def delete_history(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        # Получаем последнюю запись в истории и удаляем ее
        latest_history_item = database_service.get_history_wallet(str(user_id))

        if latest_history_item:
            database_service.delete_wallet_history(str(user_id))
            database_service.change_wallet_balance(str(user_id), 0.00)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="История была удалена."
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="История пуста."
            )


class CustomTaxHandler:
    @staticmethod
    async def create_custom_tax(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        args = context.args

        if len(args) >= 3:
            default_cost = float(args[0])
            reason = ' '.join(args[1:2])
            operation_type = args[-1].lower()
            database_service.create_custom_tax(str(user_id), reason, default_cost, operation_type)
            user_taxes = database_service.get_user_custom_taxes(str(user_id))
            buttons = []
            for tax in user_taxes:
                button_text = tax.name
                button_callback_data = json.dumps({'action': 'custom_tax_click', 'tax_id': tax.id})
                buttons.append([KeyboardButton(button_text)])

            reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

            await update.message.reply_text(
                'Ваша кнопка успешно создана!\n',
                reply_markup=reply_markup,
            )

        else:
            await update.message.reply_text('Пожалуйста, укажите стоимость, описание и тип {Выплата или оплата}')

    @staticmethod
    async def handle_custom_tax_click(update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        text = update.message.text
        tax = database_service.get_custom_tax_by_name(str(user_id), text)

        if tax:
            if tax.payment_type == 'Выплата':
                money = abs(int(tax.default_cost))
            else:
                money = -abs(int(tax.default_cost))

            database_service.change_wallet_balance(str(user_id), money)
            database_service.update_history_balance(str(user_id), 'tax_' + str(tax.id), money, tax.name)
            balance = database_service.get_balance(str(user_id))

            await update.message.reply_text(f"Запись была учтена, текущий баланс: {balance}")
        else:
            await update.message.reply_text("Команда не распознана.")
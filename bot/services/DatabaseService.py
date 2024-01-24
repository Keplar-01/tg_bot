from database import Session
from model.models import User, Wallet, WalletHistory, CustomTax
from utils.data_sources.SQLAlchemyDS import SQLAlchemyDataSource

class DatabaseService:
    def __init__(self, session):
        self.data_source = SQLAlchemyDataSource(session)

    def create_user(self, tg_user_id):
        user = User(telegram_id=str(tg_user_id))
        self.data_source.insert_item(user)
        wallet = Wallet(user_id=user.id, balance=0)
        self.data_source.insert_item(wallet)

    def get_user(self, tg_user_id):
        return self.data_source.get_item_by_filter(User, telegram_id=tg_user_id)

    def get_wallet(self, user_id):
        return self.data_source.get_item_by_filter(Wallet, user_id=user_id)

    def get_balance(self, tg_user_id):
        user = self.get_user(tg_user_id)
        wallet = self.get_wallet(user.id)
        return wallet.balance

    def change_wallet_balance(self, tg_user_id, amount):
        user = self.get_user(tg_user_id)
        wallet = self.get_wallet(user.id)
        wallet.balance += int(amount)
        self.data_source.commit()

    def update_history_balance(self, tg_user_id, operation_type, money, message):
        user = self.get_user(tg_user_id)
        wallet = self.get_wallet(user.id)
        record_history = WalletHistory(
            wallet_id=wallet.id,
            description=message,
            amount=money,
            operation_type=operation_type
        )
        self.data_source.insert_item(record_history)
        self.data_source.commit()

    def get_history_wallet(self, tg_user_id):
        user = self.get_user(tg_user_id)
        wallet = self.get_wallet(user.id)
        return self.data_source.get_list_by_filter(WalletHistory, wallet_id=wallet.id)

    def delete_user_info(self, tg_user_id):
        user = self.get_user(tg_user_id)
        wallet = self.get_wallet(user.id)
        self.data_source.delete_items_by_filter(WalletHistory, wallet_id=wallet.id)

        self.data_source.delete_item(wallet)
        self.data_source.delete_item(user)

        self.data_source.commit()

    def change_wallet_history(self, tg_user_id, new_data):
        user = self.get_user(tg_user_id)
        wallet = self.get_wallet(user.id)

        history_item_id = new_data.get('history_item_id')
        updated_description = new_data.get('updated_description')
        updated_amount = new_data.get('updated_amount')

        if history_item_id is not None and (updated_description is not None or updated_amount is not None):
            history_item = self.data_source.get_item(WalletHistory, history_item_id)

            if history_item:
                if updated_description is not None:
                    history_item.description = updated_description
                if updated_amount is not None:
                    history_item.amount = updated_amount

                self.data_source.update_item(history_item)

    def delete_wallet_history(self, tg_user_id):
        user = self.get_user(tg_user_id)
        wallet = self.get_wallet(user.id)
        self.data_source.delete_items_by_filter(WalletHistory, wallet_id=wallet.id)

        self.data_source.commit()

    def create_custom_tax(self, user_id, name, default_cost, payment_type):
        custom_tax = CustomTax(name=name, default_cost=default_cost, payment_type=payment_type, user_id=self.get_user(user_id).id)
        self.data_source.insert_item(custom_tax)
        self.data_source.commit()
        return custom_tax.id

    def get_user_custom_taxes(self, user_id):
        return self.data_source.get_list_by_filter(CustomTax, user_id=self.get_user(user_id).id)

    def get_custom_tax_by_id(self, custom_tax_id, name):
        return self.data_source.get_item_by_filter(CustomTax, id=custom_tax_id)

    def get_custom_tax_by_name(self, user_id, name):
        user = self.data_source.get_item_by_filter(User, telegram_id=user_id)
        return self.data_source.get_item_by_filter(CustomTax, user_id=user.id, name=name)
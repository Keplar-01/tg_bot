from abc import ABC

from telegram import Update
from telegram.ext import CallbackContext


class CommandInterface(ABC):
    async def execute(self, update: Update, context: CallbackContext):
        raise NotImplementedError("Subclasses must implement")

    def get_name(self):
        raise NotImplementedError("Subclasses must implement")
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager

from tgbot.misc.states import BotMenuStates


async def command_menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(BotMenuStates.select_categories)


def register_user(dp: Dispatcher):
    dp.message.register(command_menu, Command("menu"))

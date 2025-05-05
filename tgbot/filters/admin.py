import logging
import typing

from aiogram import Bot, Dispatcher
from aiogram.filters import  BaseFilter
from aiogram.types import Message

from tgbot.config import Config


class AdminFilter(BaseFilter):

    def __init__(self, is_admin: typing.Optional[bool] = None) -> None:
        self.is_admin = is_admin

    async def __call__(self, message: Message, config) -> bool:
        if self.is_admin is None:
            return False
        config: Config = config
        return (message.from_user.id in config.tg_bot.admin_ids) == self.is_admin
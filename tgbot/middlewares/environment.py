import logging
from typing import Dict, Any, Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class EnvironmentMiddleware(BaseMiddleware):

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.skip_patterns = ["error", "update"]

    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data:[Dict[str, Any]], *args) -> Any:
        if event.event_type in self.skip_patterns:
            return await handler(event, data)
        data.update(**self.kwargs)
        return await handler(event, data)

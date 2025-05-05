import asyncio
import json
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from redis import Redis

from tgbot.config import load_config
from tgbot.dialogs import setup_dialogs2
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware
from tgbot.services.repo import Repo
logger = logging.getLogger(__name__)


def register_all_middlewares(dp: Dispatcher, config, repo):
    dp.update.outer_middleware(EnvironmentMiddleware(config=config, repo=repo))


def register_all_filters(dp: Dispatcher):
    dp.message.filter(AdminFilter(is_admin=True))


def register_all_handlers(dp: Dispatcher):
    register_user(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    # redis = Redis()

    storage = RedisStorage() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=storage)

    dp['config'] = config
    with open('tgbot/misc/test_data.json', 'r', encoding='utf-8') as f:
        repo = Repo(test_data=json.load(f))

    register_all_middlewares(dp, config, repo)
    register_all_filters(dp)
    register_all_handlers(dp)
    setup_dialogs2(dp)

    # start
    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

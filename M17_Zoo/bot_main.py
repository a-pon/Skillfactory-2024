import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import Message
# from aiogram import F
# from aiogram.utils.formatting import as_list, as_marked_section, Bold
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from token_data import TOKEN
from bot_handler import router

dp = Dispatcher()
dp.include_router(router)


@dp.message(CommandStart())
async def bot_start(message: Message) -> None:
    await message.answer(
        'Добро пожаловать на викторину, где Вы узнаете своё тотемное животное!\n\n'
        '/quiz_start'
)


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    # logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

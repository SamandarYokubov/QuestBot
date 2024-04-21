import asyncio
import logging

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from config_reader import config 

from handlers import common, courses, about, modules, progress, questions

async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command='start', description='Start Bot')
    ]
    await bot.set_my_commands(commands)


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

bot = Bot(config.bot_token.get_secret_value())

storage = RedisStorage.from_url('redis://62.171.186.99:6379/0')

dp = Dispatcher(storage=storage)

async def main():

    dp.include_router(common.router)  
    dp.include_router(courses.router)
    dp.include_router(about.router)
    dp.include_router(modules.router)
    dp.include_router(progress.router)
    dp.include_router(questions.router) 

    
    await set_bot_commands(bot)

    await dp.start_polling(bot, skip_updates=True, on_shutdown=on_shutdown)



async def on_shutdown(dp: Dispatcher):
    await dp.storage_close()
    await dp.storage.wait_closed()



if __name__ == '__main__':
    asyncio.run(main())
from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import CommandStart, Filter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.markdown import hbold

# from bot.data_storage import DataStorage, UserData
from bot.settings import Settings
from bot.states import states_router, Initial


dp = Dispatcher()


async def command_start_handler(message: Message, state: FSMContext) -> None:
    await Initial.main_menu.init(message, state)
    await state.set_state(state=Initial.main_menu)


class KnowledgeBot:
    bot: Bot
    dispatcher: Dispatcher

    def __init__(self, settings: Settings):
        self.bot = Bot(settings.telegram_bot_token)
        self.dispatcher = dp

        start_router = Router()
        start_router.message.register(command_start_handler, CommandStart())
        start_router.message.register(command_start_handler, lambda msg: msg.text)

        dp.include_router(states_router)
        dp.include_router(start_router)


    async def on_startup(self, dispatcher: Dispatcher):
        pass

    async def on_shutdown(self, dispatcher: Dispatcher):
        pass

    async def run(self):
        await self.dispatcher.start_polling(self.bot, skip_updates=True, on_startup=self.on_startup,
                               on_shutdown=self.on_shutdown)

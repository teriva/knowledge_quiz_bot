from typing import Optional

from aiogram import types


from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.storage.base import StorageKey

from bot.data_storage import UserData


class BaseCustomState(State):

    @staticmethod
    def _get_user_data_key(message: types.Message) -> StorageKey:
        return StorageKey(
            bot_id=message.bot.id,
            chat_id=message.chat.id,
            user_id=message.from_user.id,
        )

    async def get_user_data(self, message: types.Message, state: FSMContext) -> UserData:
        raw_data: dict = await state.storage.get_data(self._get_user_data_key(message))
        if raw_data == {}:
            user_data = UserData(id=message.from_user.id, language_code=message.from_user.language_code, )
        else:
            user_data = UserData.from_dict(await state.storage.get_data(self._get_user_data_key(message)))
        return user_data

    async def set_user_date(self, message: types.Message, state: FSMContext, new_user_data: UserData):
        print('======', new_user_data)
        await state.storage.set_data(key=self._get_user_data_key(message), data=new_user_data.to_dict())

    async def init(self, message: types.Message, state: Optional[FSMContext]):
        pass

    async def processing(self, message: types.Message, state: Optional[FSMContext]):
        pass


    @classmethod
    async def set_state(cls, message: types.Message, state: FSMContext = None, new_state=None):
        print(f'------------- SET STATE ------------- {await state.get_state()} -> {new_state}, {type(new_state)}')

        await new_state.init(message=message, state=state)
        await state.set_state(state=new_state)

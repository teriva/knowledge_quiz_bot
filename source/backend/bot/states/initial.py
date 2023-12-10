from typing import Optional

from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.data_storage import UserData
from bot.states.base import BaseCustomState
from bot.states.quizzes import Quizzes
from bot.text import EnglishText, languages



class MainMenuState(BaseCustomState):

    async def get_keyboard(self, text: EnglishText) -> ReplyKeyboardMarkup:
        main_menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [KeyboardButton(text=text.start_quizzes_button_name)],
                [KeyboardButton(text=text.change_language_button_name)],

            ], selective=True
        )
        return main_menu_keyboard

    async def init(self, message: types.Message, state: Optional[FSMContext]):
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)
        await message.bot.send_message(
            message.chat.id, language_text.select_action_message, reply_markup=await self.get_keyboard(language_text)
        )

    async def processing(self, message: types.Message, state: Optional[FSMContext]):
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)

        if message.text == language_text.change_language_button_name:
            await BaseCustomState.set_state(message=message, state=state, new_state=Initial.choice_language)
        elif message.text == language_text.start_quizzes_button_name:
            await BaseCustomState.set_state(message=message, state=state, new_state=Quizzes.upload_file)
        else:
            await message.bot.send_message(
                message.chat.id, language_text.error_choice_message_name,
                reply_markup=await self.get_keyboard(language_text)
            )


class ChoiceLanguageState(BaseCustomState):
    keyboard = []
    for langua in languages.all:
        langua_button = KeyboardButton(text=f'{langua.language_name} {langua.flag}')
        keyboard.append(langua_button)

    choice_language_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
        keyboard=[keyboard], resize_keyboard=True, selective=True
    )

    async def init(self, message: types.Message, state: Optional[FSMContext]):
        user_data: UserData = await self.get_user_data(message, state)
        current_language_text: EnglishText = languages.get_by_code(user_data.language_code)

        await message.bot.send_message(
            message.chat.id, current_language_text.choice_language_message, reply_markup=self.choice_language_keyboard
        )

    async def processing(self, message: types.Message, state: Optional[FSMContext]):
        user_data: UserData = await self.get_user_data(message, state)
        split_text: list = message.text.split(' ')
        language_name = split_text[0] if len(split_text) > 0 else ''

        new_language_text: Optional[EnglishText] = languages.get_by_name(language_name)

        if not new_language_text:
            current_language_text: EnglishText = languages.get_by_code(user_data.language_code)
            await message.bot.send_message(
                message.chat.id, current_language_text.error_choice_message_name, reply_markup=self.choice_language_keyboard
            )
            return

        user_data.language_code = new_language_text.language_code
        await self.set_user_date(message, state, user_data)
        await message.bot.send_message(message.chat.id, new_language_text.successfully_change_language_message)

        await BaseCustomState.set_state(message=message, state=state, new_state=Initial.main_menu)


class Initial(StatesGroup):
    choice_language = ChoiceLanguageState()
    main_menu = MainMenuState()

router = Router()

router.message.register(Initial.main_menu.processing, Initial.main_menu)
router.message.register(Initial.choice_language.processing, Initial.choice_language)


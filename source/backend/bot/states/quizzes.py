from io import BytesIO
from typing import Optional

import PyPDF2
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from gigachat import GigaChat
from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.prompts import PromptTemplate

from bot.data_storage import UserData
from bot.generage_test import generate_test
from bot.settings import settings
from bot.states import BaseCustomState
from bot.text import EnglishText, languages

def getText(path):
  text=""
  with open(path,"rb") as file:
    pdf=PyPDF2.PdfReader(file)
    pages=len(pdf.pages)
    for i in range(pages):
      page=pdf.pages[i]
      text+=page.extract_text()
  return text


class UploadFileState(BaseCustomState):

    async def get_keyboard(self, text: EnglishText) -> ReplyKeyboardMarkup:
        main_menu_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            resize_keyboard=True, keyboard=[
                [KeyboardButton(text=text.return_to_main_menu)],
            ], selective=True
        )
        return main_menu_keyboard

    async def init(self, message: types.Message, state: Optional[FSMContext]):
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)
        await message.bot.send_message(
            message.chat.id, language_text.load_pdf_file_message, reply_markup=await self.get_keyboard(language_text)
        )

    def get_user_file_path(self, message: types.Message) -> str:
        return f'storage/{message.from_user.id}.pdf'

    async def download_file(self, message: types.Message):
        file: BytesIO = await message.bot.download(
            message.document
        )
        with open(self.get_user_file_path(message), "wb") as f:
            f.write(file.getbuffer())

    async def processing(self, message: types.Message, state: Optional[FSMContext]):
        from bot.states import Initial
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)

        if message.text == language_text.return_to_main_menu:
            await BaseCustomState.set_state(message=message, state=state, new_state=Initial.main_menu)
            return

        if message.document is None:
            await message.bot.send_message(message.chat.id, language_text.load_pdf_file_message)
            return

        await self.download_file(message)

        await message.bot.send_message(message.chat.id, language_text.document_loaded)
        await BaseCustomState.set_state(message=message, state=state, new_state=Quizzes.set_questions_count)


class SetQuestionsCount(UploadFileState):
    async def init(self, message: types.Message, state: Optional[FSMContext]):
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)
        await message.bot.send_message(
            message.chat.id, language_text.set_questions_count_message, reply_markup=await self.get_keyboard(language_text)
        )

    async def processing(self, message: types.Message, state: Optional[FSMContext]):
        from bot.states import Initial
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)

        if message.text == language_text.return_to_main_menu:
            await BaseCustomState.set_state(message=message, state=state, new_state=Initial.main_menu)
            return

        if not message.text.isdigit():
            await message.bot.send_message(
                message.chat.id, language_text.set_questions_count_message,
                reply_markup=await self.get_keyboard(language_text)
            )

        user_data.question_count = int(message.text) if int(message.text) < 10 else 10

        await BaseCustomState.set_state(message=message, state=state, new_state=Quizzes.start_quiz)


class StartQuiz(UploadFileState):
    async def init(self, message: types.Message, state: Optional[FSMContext]):
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)
        await message.bot.send_message(
            message.chat.id, language_text.star_quiz_message, reply_markup=await self.get_keyboard(language_text)
        )

        response_schemas = [
            ResponseSchema(name="question",
                           description="A multiple choice question generated from input text snippet."),
            ResponseSchema(name="options", description="Possible choices for the multiple choice question."),
            ResponseSchema(name="answer", description="Correct answer for the question.")
        ]

        # The parser that will look for the LLM output in my schema and return it back to me
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # The format instructions that LangChain makes. Let's look at them
        format_instructions = output_parser.get_format_instructions()

        chat_model = GigaChat(
            credentials=settings.gigachat_credential,
            verify_ssl_certs=False
        )

        # The prompt template that brings it all together
        prompt_template = PromptTemplate.from_template(
            "From the text {theTextT} generate {number} multiple choice questions with their correct answers in {lang} in JSON format"
        )

        text = getText(self.get_user_file_path(message))

        newnew = prompt_template.format_prompt(
            number=str(user_data.questions_count), theTextT=text, lang=user_data.language_code
        )

        user_query_output = chat_model(newnew.to_messages())

        return user_query_output.content, text

    async def processing(self, message: types.Message, state: Optional[FSMContext]):
        from bot.states import Initial
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)

        if message.text == language_text.return_to_main_menu:
            await BaseCustomState.set_state(message=message, state=state, new_state=Initial.main_menu)
            return

        await message.bot.send_message(
            message.chat.id, language_text.star_quiz_message, reply_markup=await self.get_keyboard(language_text)
        )


class Quizzes(StatesGroup):
    upload_file = UploadFileState()
    set_questions_count = SetQuestionsCount()
    start_quiz = StartQuiz()


router = Router()
router.message.register(Quizzes.upload_file.processing, Quizzes.upload_file)
router.message.register(Quizzes.set_questions_count.processing, Quizzes.set_questions_count)
router.message.register(Quizzes.start_quiz.processing, Quizzes.start_quiz)

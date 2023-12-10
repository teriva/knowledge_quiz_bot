import json
from io import BytesIO
from typing import Optional

import PyPDF2
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from langchain.output_parsers import ResponseSchema, StructuredOutputParser
from langchain_core.messages import SystemMessage, AIMessage
from langchain_core.prompts import PromptTemplate

from bot.data_storage import UserData
from bot.generage_test import generate_test
from bot.settings import settings, chat_model
from bot.states import BaseCustomState
from bot.text import EnglishText, languages
from langchain.chat_models.gigachat import GigaChat

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

        question_count = int(message.text)

        if question_count > 10:
            question_count = 10
        if question_count < 1:
            question_count = 1

        user_data.current_question = 0
        user_data.questions_count = question_count

        await self.set_user_date(message, state, user_data)

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
            ResponseSchema(name="answer", description="Correct answer for the question.")
        ]

        # The parser that will look for the LLM output in my schema and return it back to me
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)

        # The format instructions that LangChain makes. Let's look at them
        format_instructions = output_parser.get_format_instructions()


        # The prompt template that brings it all together
        prompt_template = PromptTemplate.from_template(
            "From the text {theTextT} generate {number} multiple choice questions with their correct answers "
            "in {lang}. ответ должен быть в формате json, список объектов. "
            "Каждый из объектов содержит поле question и answer, response example: [{example}]"
        )

        text = getText(self.get_user_file_path(message))

        newnew = prompt_template.format_prompt(
            number=str(user_data.questions_count), theTextT=text, lang=language_text.language_name,
            example='{"question": "some text", "answer": "some text"}'
        )

        print('-----', newnew.to_messages())

        user_query_output = chat_model(newnew.to_messages())
        print(')))))))',user_query_output.content)
        questions: dict = json.loads(user_query_output.content)

        user_data.questions = questions
        # user_data.questions = [{'question': 'What is a computer?', 'answer': 'An electronic device that processes data through logical and arithmetic operations.'}, ]
        await self.set_user_date(message, state, user_data)

        await message.bot.send_message(
            message.chat.id, language_text.answer_question.format(
                question=user_data.questions[user_data.current_question].get('question')),
            reply_markup=await self.get_keyboard(language_text)
        )

    async def processing(self, message: types.Message, state: Optional[FSMContext]):
        from bot.states import Initial
        user_data: UserData = await self.get_user_data(message, state)
        language_text: Optional[EnglishText] = languages.get_by_code(user_data.language_code)

        if message.text == language_text.return_to_main_menu:
            await BaseCustomState.set_state(message=message, state=state, new_state=Initial.main_menu)
            return

        question = user_data.questions[user_data.current_question]['question']
        answer = user_data.questions[user_data.current_question].get('answer')

        message_for_model = """
        
        
        Did the user answer the question correctly? YOUR RESPONSE SHOULD BE IN THE FORM OF JSON IN THE FOLLOWING FORMAT: {format} 
        
        in the "why" field, you need to write a detailed message why the answer is wrong in the language: {lang},
         or additions to the user's answer if the answer is correct, 
    
         
        The user was answering the following question: {question}
        Approximate correct answer: {answer}
        The answer given by the user: {user_answer}
        
        YOU MAST EVALUATE THE USER'S RESPONSE, IT'S EASIER NOT TO FIND FAULT WITH THE LACK OF DETAILS, OR AN INCOMPLETE ANSWER.
        
        
         
        """.format(question=question, answer=answer, user_answer=message.text,
                   format='{"answer_is_correct": {bool value}, "why": ""}',
                   lang=language_text.language_name
                   )


        response: AIMessage = chat_model([SystemMessage(content=message_for_model)])


        try:
            data = json.loads(response.content)
        except Exception:
            data = {"answer_is_correct": True, "why": ""}


        user_data.current_question += 1
        await self.set_user_date(message, state, user_data)

        if data['answer_is_correct'] == False:
            await message.bot.send_message(
                message.chat.id, data.get("why"),
                reply_markup=await self.get_keyboard(language_text)
            )
        else:
            await message.bot.send_message(
                message.chat.id, language_text.answer_is_correct.format(more=data.get("why")),
                reply_markup=await self.get_keyboard(language_text)
            )
            user_data.current_question += 1

        if user_data.current_question >= len(user_data.questions):
            user_data.current_question -= 1
            await message.bot.send_message(
                message.chat.id, language_text.quiz_completed.format(
                    all=len(user_data.questions), correct=user_data.correct_answers
                ),
                reply_markup=await self.get_keyboard(language_text)
            )
            await BaseCustomState.set_state(message=message, state=state, new_state=Initial.main_menu)
            return

        await message.bot.send_message(
            message.chat.id, language_text.answer_question.format(
                question=user_data.questions[user_data.current_question].get('question')),
            reply_markup=await self.get_keyboard(language_text)
        )


class Quizzes(StatesGroup):
    upload_file = UploadFileState()
    set_questions_count = SetQuestionsCount()
    start_quiz = StartQuiz()


router = Router()
router.message.register(Quizzes.upload_file.processing, Quizzes.upload_file)
router.message.register(Quizzes.set_questions_count.processing, Quizzes.set_questions_count)
router.message.register(Quizzes.start_quiz.processing, Quizzes.start_quiz)

from aiogram import Router

from bot.states.base import BaseCustomState


from bot.states.initial import Initial
from bot.states.test import TestState

from bot.states.initial import router as initial_router
from bot.states.quizzes import router as quizzes_router

states_router = Router()
states_router.include_router(initial_router)
states_router.include_router(quizzes_router)

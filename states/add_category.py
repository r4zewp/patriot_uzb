from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class NewCategory(StatesGroup):
    name_ru = State()
    name_uz = State()
    isSexNeeded = State()
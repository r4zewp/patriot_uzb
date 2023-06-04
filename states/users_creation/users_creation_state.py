from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class UserCreationState(StatesGroup):
    lang = State()
    name = State()
    phone = State()
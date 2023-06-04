from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class NewItemStates(StatesGroup):
    category = State()
    name = State()
    sex = State()
    color = State()
    art = State()
    size = State()
    price = State()
    ikpu = State()
    units_code = State()
    package_code = State()
    first = State()
    second = State()
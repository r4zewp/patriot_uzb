from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class ChooseCategories(StatesGroup):
    idle = State()
    choosing_item = State()
    choosing_category = State()
    choosing_sex = State()
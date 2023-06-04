from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class AddingAdmin(StatesGroup):
    fwd_message = State()
    success = State()
    fail = State()
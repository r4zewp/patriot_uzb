from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

class OrderConfirm(StatesGroup):
    type=State()
    location=State()
    payment=State()
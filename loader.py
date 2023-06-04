from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db.db import *
from data import config
import logging

logging.basicConfig()
storage = MemoryStorage()
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=storage)
db = DatabaseManager(config.DATABASE)
db.create_tables()
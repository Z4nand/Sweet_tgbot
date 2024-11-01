import logging
from aiogram import Bot, Dispatcher


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

API_TOKEN = '8048142145:AAEzLxL9ChlKTS_692lR19TP69w3uqTHLNU'


# Объект бота
bot = Bot(token=API_TOKEN)

# Диспетчер
dp = Dispatcher()
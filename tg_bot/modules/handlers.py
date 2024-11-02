from .dispatcher import dp
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from modules.quiz.quiz import new_quiz
from aiogram import F
from .sql.database import get_rate
from .quiz.quiz_question import quiz_data

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))



# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):

    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)


# Хэндлер на команду /rate
@dp.message(Command("rate"))
async def cmd_rate(message: types.Message):
    rate_data = await get_rate(message.from_user.id)  # Запрос данных из БД

    if rate_data:
        await message.answer(f"{rate_data}/{len(quiz_data)}")
    else:
        await message.answer("Нет данных о рейтингах.")
    
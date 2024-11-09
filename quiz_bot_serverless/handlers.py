from aiogram import types, Dispatcher, F, Router
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject, CREATOR
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from database import get_quiz_data
from service import generate_options_keyboard, get_question, new_quiz, get_quiz_index, update_quiz_index, get_rate

IMAGE_URL = 'https://storage.yandexcloud.net/img-tgbot/quiz_img.jpg'

router = Router()

@router.callback_query()
async def check_answer(callback: types.CallbackQuery):
    quiz_data  = await get_quiz_data()
    user_answer = callback.data  # Получаем выбор пользователя
    current_question_index = await get_quiz_index(callback.from_user.id)
    correct_index = quiz_data[current_question_index]['correct_option']
    correct_answer = quiz_data[current_question_index]['options'][correct_index]
    rate = await get_rate(callback.from_user.id)


    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    
    await callback.message.answer(f"Вы выбрали: {user_answer}")  # Печатаем выбранный ответ пользователя

    if user_answer == correct_answer:
        await callback.message.answer("Верно!")
        rate +=1
    else:
        await callback.message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

    # Обновление номера текущего вопроса в базе данных
    current_question_index += 1
   
    await update_quiz_index(callback.from_user.id, current_question_index, rate)
    
    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        await callback.message.answer(f"Ваш рейтинг: {await get_rate(callback.from_user.id)}/{len(quiz_data)}")


# Хэндлер на команду /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команду /quiz
@router.message(F.text=="Начать игру")
@router.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer_photo(photo=IMAGE_URL) #img начало квиза
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)
    

# Хэндлер на команду /rate
@router.message(Command("rate"))
async def cmd_rate(message: types.Message):
    quiz_data = await get_quiz_data()
    rate_data = await get_rate(message.from_user.id)  # Запрос данных из БД

    if rate_data:
        await message.answer(f"{rate_data}/{len(quiz_data)}")
    else:
        await message.answer("Нет данных о рейтингах.")

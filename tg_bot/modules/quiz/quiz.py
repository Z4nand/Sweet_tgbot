from aiogram import types
from aiogram import F
from aiogram.utils.keyboard import InlineKeyboardBuilder

from modules.dispatcher import dp
from modules.sql.database import update_quiz_index, get_quiz_index, get_rate
from .quiz_question import quiz_data



def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=option  # Используем текст опции в качестве callback_data(вместо того, чтобы разделять на прав/неправ)
        ))
    builder.adjust(1)
    return builder.as_markup()

async def get_question(message, user_id):
    # Получение текущего вопроса из словаря состояний пользователя
    current_question_index = await get_quiz_index(user_id)
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts)  # Убираем правильный ответ, добавляя все опции
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    rate = 0
    await update_quiz_index(user_id, current_question_index, rate)
    await get_question(message, user_id)

@dp.callback_query()
async def check_answer(callback: types.CallbackQuery):
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

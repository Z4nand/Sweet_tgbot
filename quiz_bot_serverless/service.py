from  database import pool, execute_update_query, execute_select_query
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from database import get_quiz_data


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
    quiz_data = await get_quiz_data()
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


async def get_quiz_index(user_id):
    get_user_index = f"""
        DECLARE $user_id AS Uint64;

        SELECT question_index
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_index, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["question_index"] is None:
        return 0
    return results[0]["question_index"]    


async def get_rate(user_id):
    get_user_index = f"""
        DECLARE $user_id AS Uint64;

        SELECT rate
        FROM `quiz_state`
        WHERE user_id == $user_id;
    """
    results = execute_select_query(pool, get_user_index, user_id=user_id)

    if len(results) == 0:
        return 0
    if results[0]["rate"] is None:
        return 0
    return results[0]["rate"]   
    

async def update_quiz_index(user_id, question_index, rate):
    set_quiz_state = f"""
        DECLARE $user_id AS Uint64;
        DECLARE $question_index AS Uint64;
        DECLARE $rate AS Uint64;

        UPSERT INTO `quiz_state` (`user_id`, `question_index`,`rate`)
        VALUES ($user_id, $question_index, $rate);
    """

    execute_update_query(
        pool,
        set_quiz_state,
        user_id=user_id,
        question_index=question_index,
        rate = rate,
    )
    

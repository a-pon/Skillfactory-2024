import json
import os.path

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from quiz_data import questions, answers

router = Router()


class QuizData(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    contact = State()
    feedback = State()


@router.message(Command('quiz_start'))
async def handle_first_question(message: Message, state: FSMContext):
    kb = [
        [
            types.KeyboardButton(text=answers[0][0]),
            types.KeyboardButton(text=answers[0][1]),
            types.KeyboardButton(text=answers[0][2]),
            types.KeyboardButton(text=answers[0][3]),
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await message.answer(questions[0], reply_markup=keyboard)
    await state.set_state(QuizData.question1.state)


@router.message(QuizData.question1)
async def handle_second_question(message: Message, state: FSMContext):
    if message.text not in answers[0]:
        await message.answer('Выберите ответ из предложенных вариантов')
    else:
        await state.set_data({'answer1': message.text})
        kb = [
            [
                types.KeyboardButton(text=answers[1][0]),
                types.KeyboardButton(text=answers[1][1]),
                types.KeyboardButton(text=answers[1][2]),
                types.KeyboardButton(text=answers[1][3]),
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.answer(questions[1], reply_markup=keyboard)
        await state.set_state(QuizData.question2.state)


@router.message(QuizData.question2)
async def handle_third_question(message: Message, state: FSMContext):
    if message.text not in answers[1]:
        await message.answer('Выберите ответ из предложенных вариантов')
    else:
        await state.update_data({'answer2': message.text})
        kb = [
            [
                types.KeyboardButton(text=answers[2][0]),
                types.KeyboardButton(text=answers[2][1]),
                types.KeyboardButton(text=answers[2][2]),
                types.KeyboardButton(text=answers[2][3]),
            ]
        ]
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=kb,
            resize_keyboard=True
        )
        await message.answer(questions[2], reply_markup=keyboard)
        await state.set_state(QuizData.question3.state)


@router.message(QuizData.question3)
async def show_share_result(message: Message, state: FSMContext):
    if message.text not in answers[2]:
        await message.answer('Выберите ответ из предложенных вариантов')
    else:
        await state.update_data({'answer3': message.text})
        data = await state.get_data()
        result = []
        for i in range(3):
            result.append(answers[i].index(data[f'answer{i+1}']))
        if 0 <= sum(result) < 3:
            totem = 'Амурский тигр'
        elif sum(result) < 6:
            totem = 'Енот-полоскун'
        else:
            totem = 'Росомаха'
        await state.update_data({'totem': totem})
        share_message = f'Моё тотемное животное - {totem}!\
            \nУзнайте своё, пройдя викторину в Telegram-боте: https://t.me/MosZoo_Quiz_Bot'
        vk_link = f'https://vk.com/share.php?url=https://t.me/MosZoo_Quiz_Bot&title={share_message}'
        photo_path = os.path.join(os.getcwd(), 'photos', f'{totem}.jpg')
        kb = [
            [InlineKeyboardButton(text='Связаться с сотрудником', callback_data='contact')],
            [InlineKeyboardButton(text='Оставить отзыв', callback_data='feedback')],
            [InlineKeyboardButton(text='Поделиться в VK', url=vk_link)],
        ]
        inlinekb = InlineKeyboardMarkup(inline_keyboard=kb)
        await message.answer_photo(
            photo=types.FSInputFile(photo_path),
            caption=f'Ваше тотемное животное - {totem}!\n\n'
                    'Чтобы узнать больше о программе опекунства, '
                    'Вы можете связаться с нашим сотрудником по кнопке ниже',
            reply_markup=inlinekb
        )
        await message.answer('Попробовать ещё раз?\n/quiz_start', reply_markup=types.ReplyKeyboardRemove())


@router.callback_query(F.data == 'contact')
async def contact(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    kb = [[types.KeyboardButton(text=f'Результат викторины: {data['totem']}')]]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await callback_query.message.answer(
        'Контакты сотрудника\n\n'
        'E-mail: staff@zoo.mail\n'
        'Телефон: +7-123-456-78-90\n'
        'Чат в Telegram по кнопке ниже:',
        reply_markup=keyboard
    )
    await state.set_state(QuizData.contact.state)


@router.message(QuizData.contact)
async def text_to_staff(message: Message):
    # Вместо chat_id подставить id сотрудника
    await message.copy_to(chat_id=message.chat.id, reply_markup=types.ReplyKeyboardRemove())


@router.callback_query(F.data == 'feedback')
async def feedback(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.answer(
        'Напишите Ваш отзыв ниже, мы обязательно его прочтём\n',
        reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(QuizData.feedback.state)


@router.message(QuizData.feedback)
async def save_feedback(message: Message):
    with open('feedback.json', 'a', encoding='utf8') as file:
        fb = {
            'user': message.from_user.username,
            'feedback': message.text,
        }
        fb = json.dumps(fb, indent=4, ensure_ascii=False)
        file.write(fb)
    await message.answer('Спасибо за Ваш отзыв')

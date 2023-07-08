import logging

import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import sqlite3
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

db = sqlite3.connect(database='database.db', check_same_thread=False)
cur = db.cursor()

class Sates(StatesGroup):
    for_otvet = State()
    wait = State()

API_TOKEN = '6089977922:AAHbw7QIcsjnnVrJ31oMx_04_1UdJQqPQs0'


logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

pred = [["Руский", "russian"], ["Математика", "math"], ["Литература", "literature"], ["Английский язык", "english"], ["История", "history"], ["Обществознание", "social"], ["География", "geography"], ["Биология", "biology"], ["Физика", "physics"], ["Химия", "chemistry"], ["Информатика", "informatics"], ["Физкультура", "pe"]]
calls = [el[1] for el in pred]



@dp.message_handler(commands=['start'])
async def start(mesage: types.Message):
    #check if user already exists in database
    check = cur.execute("SELECT tg_id FROM users WHERE tg_id =?", (mesage.from_user.id,)).fetchone()
    if check is not None:
        kb_1 = KeyboardButton(text="Создать запись")
        kb_2 = KeyboardButton(text="Просмотреть записи")
        kb = ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add(kb_1).add(kb_2)
        await mesage.answer("Поздравляю вы зарегестрированы!! \n Можете начинать делиться и получать ответы", reply_markup=kb)
    else:
        print(mesage.from_user.id)
        button_text = "Зарегестрироваться"
        button_callback = "register"
        inline_keyboard = InlineKeyboardMarkup(row_width=1)
        register_button = InlineKeyboardButton(button_text, callback_data=button_callback)
        inline_keyboard.insert(register_button)
        await mesage.answer("Вы не зарегестрированы!!", reply_markup=inline_keyboard)

@dp.callback_query_handler()
async def call(call: types.CallbackQuery):
    if call.data == "register":
        cur.execute("INSERT INTO users (tg_id, username) VALUES(?, ?)", (call.from_user.id, call.from_user.username))
        db.commit()
        await call.message.answer("Успешная регестрация нажмите /start чтобу продолжить")
    if call.data in calls:
        a="False"
        cur.execute("INSERT INTO otveti (object, autor_id, posted) VALUES(?, ?, ?)", (call.data, call.from_user.id, a))
        db.commit()
        await call.message.answer("Выпишите ответы\nВ будущем будут добавлены фотографии!")
        Sates.for_otvet.set()




@dp.message_handler(lambda call: True)
async def reply_kb(message: types.Message):
    if message.text == "Создать запись":
        global pred
        global calls

        rem = ReplyKeyboardRemove()
        n = 0
        inline_keyboard = InlineKeyboardMarkup(row_width=1)
        pred = [["Руский", "russian"], ["Математика", "math"], ["Литература", "literature"], ["Английский язык", "english"], ["История", "history"], ["Обществознание", "social"], ["География", "geography"], ["Биология", "biology"], ["Физика", "physics"], ["Химия", "chemistry"], ["Информатика", "informatics"], ["Физкультура", "pe"]]
        calls = [el[1] for el in pred]

        inline_keyboard_buttons = []

        for item in pred:
            button = InlineKeyboardButton(text=item[0], callback_data=item[1])
            inline_keyboard_buttons.append(button)
        print(inline_keyboard_buttons)
        inline_keyboard.add(*inline_keyboard_buttons) # Add the buttons to the inline keyboard

        await message.answer("Выберете предмет", reply_markup=inline_keyboard)







if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)



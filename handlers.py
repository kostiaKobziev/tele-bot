import hashlib
import sqlite3
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
import aiogram.utils.markdown as md

from config import BOT_TOKEN
from main import bot, dp
import sqlite3 as sql
from aiogram.types import \
    KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from itertools import groupby
from aiogram.types import Message, CallbackQuery, ParseMode, ReplyKeyboardMarkup
import keyboards as kb
from cloudipsp import Api, Checkout
import requests
import json
import time


api = Api(merchant_id=1396424,
          secret_key='test')

checkout = Checkout(api=api)

now = datetime.datetime.now()
s = []
admin_log = False
true_pass = '1'


# Хэндлер на текстовое сообщение с текстом “Отмена”
@dp.message_handler(lambda message: message.text == "Контакти")
async def Contact(message: Message):
    con = sqlite3.connect('main_text.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM text WHERE text_slug = 'Contact_text'")
        rows = cur.fetchall()
        for row in rows:
            text = row[2]
            text = str(text).replace("\\n", '\n')
    con.commit()
    cur.close()
    await bot.send_message(chat_id=message.from_user.id, text=text)



# Отзывы

@dp.message_handler(lambda message: message.text == "Відгуки")
async def ask(message: Message):
    await bot.send_message(chat_id=message.from_user.id, text="Ви хочете прочитати відгуки або залишити його?",
                           reply_markup=kb.review_kb)


@dp.message_handler(lambda message: message.text == "Читати відгук")
async def ask(message: Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Тут відгуки наших клієнтів! \n @Resto_delivery_reviews")


class Form_reviev(StatesGroup):
    review = State()


@dp.message_handler(lambda message: message.text == "Залишити відгук")
async def cmd_start(message: Message):
    await Form_reviev.review.set()
    await bot.send_message(chat_id=message.from_user.id, text="Введіть ваш відгук")


@dp.message_handler(state=Form_reviev.review)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['review'] = message.text
        user_name = str(message.from_user.first_name)
        con = sqlite3.connect('review.db')
        cur = con.cursor()
        with con:
            cur.execute(f"INSERT INTO `review` (review_id, review_text) VALUES ('{user_name}', '{data['review']}')")
        con.commit()
        cur.close()
        await bot.send_message(chat_id=message.from_user.id, text="Ваш відгук пройде модерацію і опублікує!",
                               reply_markup=kb.greet_kb)
    await state.finish()


# КОНЕЦ Отзывы

# Часто задаваемые вопросы


@dp.message_handler(lambda message: message.text == "Часто задавані питання")
async def ask(message: Message):
    text = "Выберете интересующий вас вопрос"

    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=kb.ask_kb)


@dp.message_handler(lambda message: message.text == "Назад в меню")
async def ask(message: Message):
    text = "Вы снова в главном меню!"
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=kb.greet_kb)


@dp.message_handler(lambda message: message.text == "Часто задаваемый вопрос 1")
async def ask(message: Message):
    con = sqlite3.connect('main_text.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM text WHERE text_slug = 'q1'")
        rows = cur.fetchall()
        for row in rows:
            text = row[2]
            text = str(text).replace("\\n", '\n')
    con.commit()
    cur.close()
    await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler(lambda message: message.text == "Часто задаваемый вопрос 2")
async def ask(message: Message):
    con = sqlite3.connect('main_text.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM text WHERE text_slug = 'q2'")
        rows = cur.fetchall()
        for row in rows:
            text = row[2]
            text = str(text).replace("\\n", '\n')
    con.commit()
    cur.close()
    await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler(lambda message: message.text == "Часто задаваемый вопрос 3")
async def ask(message: Message):
    con = sqlite3.connect('main_text.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM text WHERE text_slug = 'q3'")
        rows = cur.fetchall()
        for row in rows:
            text = row[2]
            text = str(text).replace("\\n", '\n')
    con.commit()
    cur.close()
    await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler(lambda message: message.text == "Часто задаваемый вопрос 4")
async def ask(message: Message):
    con = sqlite3.connect('main_text.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM text WHERE text_slug = 'q4'")
        rows = cur.fetchall()
        for row in rows:
            text = row[2]
            text = str(text).replace("\\n", '\n')
    con.commit()
    cur.close()
    await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler(lambda message: message.text == "Часто задаваемый вопрос 5")
async def ask(message: Message):
    con = sqlite3.connect('main_text.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM text WHERE text_slug = 'q5'")
        rows = cur.fetchall()
        for row in rows:
            text = row[2]
            text = str(text).replace("\\n", '\n')
    con.commit()
    cur.close()
    await bot.send_message(chat_id=message.from_user.id, text=text)

# КОНЕЦ часто задаваемые вопросы


# создаём форму и указываем поля
class Form_reserv(StatesGroup):
    name_reserv = State()
    age = State()
    gender = State()


# Начинаем наш диалог
@dp.message_handler(lambda message: message.text == "Забронювати столик")
async def cmd_start(message: Message):
    await Form_reserv.name_reserv.set()

    await bot.send_message(chat_id=message.from_user.id, text="У скільки вас чекати? \n \n Наприклад '12:00 '", reply_markup=ReplyKeyboardRemove())

# Сюда приходит ответ с именем
@dp.message_handler(state=Form_reserv.name_reserv)
async def process_name_reserv(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_reserv'] = message.text

    await Form_reserv.next()

    await bot.send_message(chat_id=message.from_user.id, text="Ви будете один або з компанією?\n\nНаприклад '3'", reply_markup=ReplyKeyboardRemove())

# Принимаем возраст и узнаём пол
@dp.message_handler(lambda message: message.text.isdigit(), state=Form_reserv.age)
async def process_age(message: Message, state: FSMContext):
    await Form_reserv.next()
    await state.update_data(age=message.text)

    await bot.send_message(chat_id=message.from_user.id, text="Ваш номер телефону?\n\nНаприклад '1234567890'", reply_markup=ReplyKeyboardRemove())

# Сохраняем пол, выводим анкету
@dp.message_handler(state=Form_reserv.gender)
async def process_gender(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text

        await bot.send_message(
            message.chat.id,
            text="Дякую! Ми зв'яжемося з вами найближчим часом!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb.greet_kb
        )

        async def send_telegram(text: str):
            token = BOT_TOKEN
            url = "https://api.telegram.org/bot"
            channel_id = "@Resto_delivery_call_back"
            url += token
            method = url + "/sendMessage"

            r = requests.post(method, data={
                "chat_id": channel_id,
                "text": text
            })

        await send_telegram(md.text(
            md.text('#Бронірованіе_століка'),
            md.text(now.strftime("%d-%m-%Y %H:%M")),
            md.text('Час бронювання:', md.bold(data['name_reserv'])),
            md.text('Кількість людей:', md.code(data['age'])),
            md.text('Номер телефону:', data['gender']),
            sep='\n',
        ))
    await state.finish()


# создаём форму и указываем поля
class Form(StatesGroup):
    name_1 = State()
    phone = State()


# Начинаем наш диалог
@dp.message_handler(lambda message: message.text == "Зворотний дзвінок")
async def cmd_start(message: Message):
    await Form.name_1.set()

    await bot.send_message(chat_id=message.from_user.id, text="Ваше ім'я" , reply_markup=ReplyKeyboardRemove())

# Сюда приходит ответ с именем
@dp.message_handler(state=Form.name_1)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_1'] = message.text

    await Form.next()

    await bot.send_message(chat_id=message.from_user.id, text="Ваш номер телефону?\n\nНаприклад '1234567890'" , reply_markup=ReplyKeyboardRemove())


# Сохраняем пол, выводим анкету
@dp.message_handler(state=Form.phone)
async def process_phone(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

        await bot.send_message(
            message.chat.id,
            text="Дякую! Ми зв'яжемося з вами найближчим часом!",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=kb.greet_kb
        )

        async def send_telegram(text: str):
            token = BOT_TOKEN
            url = "https://api.telegram.org/bot"
            channel_id = "@Resto_delivery_call_back"
            url += token
            method = url + "/sendMessage"

            r = requests.post(method, data={
                "chat_id": channel_id,
                "text": text
            })

        await send_telegram(md.text(
            md.text('#Перезвонить'),
            md.text(now.strftime("%d-%m-%Y %H:%M")),
            md.text('ім`я:', md.bold(data['name_1'])),
            md.text('Номер телефону:', data['phone']),
            sep='\n',
        ))
    await state.finish()

@dp.message_handler(commands=['Send_to_kate'])
async def process_start_command(message: Message):
    await bot.send_message(chat_id=452317040, text="Привет, красотка!")

@dp.message_handler(commands=['start'])
async def process_start_command(message: Message):
    text = "Ласкаво просимо!"
    await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=kb.greet_kb)
    conn = sqlite3.connect('user_id.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (user_id)''')
    for u in range(0, 1):
        a1 = str(message.from_user.id)
        c.execute(f'''SELECT user_id FROM users WHERE user_id={a1}''')
        exists = c.fetchall()
        if not exists:
            c.execute(f'INSERT INTO users VALUES("{a1}")')
            conn.commit()


# создаём форму и указываем поля
class Form_prod(StatesGroup):
    cat = State()
    sub_cat = State()


# Admin Panel

# скрипт входа в админ панель
class Form_login(StatesGroup):
    passw = State()


@dp.message_handler(commands=['apl'])
async def process_start_command(message: Message):
    await Form_login.passw.set()
    await message.reply("Введіть пароль")


# Сюда приходит ответ с именем
@dp.message_handler(state=Form_login.passw)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['passw'] = message.text
        if data['passw'] == true_pass:
            await bot.send_message(chat_id=message.from_user.id, text="Пароль вірний", reply_markup=kb.admin_kb)
            global admin_log
            admin_log = True
        else:
            await bot.send_message(chat_id=message.from_user.id, text="Пароль не вірний")
            admin_log = False
    await state.finish()


# КОНЕЦ скрипта входа в админ панель

# скрипт рассылки

class Form_mess(StatesGroup):
    mess = State()


@dp.message_handler(lambda message: message.text == "Створити розсилку")
async def cmd_start(message: Message):
    if admin_log == True:
        await Form_mess.mess.set()
        await message.reply("Введіть текст для розсилки")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


@dp.message_handler(state=Form_mess.mess)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['mess'] = message.text
        users = []
        conn = sql.connect('user_id.db')
        with conn:
            cur = conn.cursor()
            cur.execute(f"SELECT * FROM users")
            rows = cur.fetchall()
            for row in rows:
                row_fix = str(row).replace('(\'', '')
                row_fix = str(row_fix).replace('\',)', '')
                users.append(str(row_fix))

            print(users)
            conn.commit()
            cur.close()
            for user_send_id_cur in users:
                await bot.send_message(chat_id=user_send_id_cur, text=data['mess'])
    await state.finish()


# КОНЕЦ скрипта рассылки

# Редактирование текстов


class Form_text_a(StatesGroup):
    text_slug = State()
    text_do = State()
    text_new_s = State()


@dp.message_handler(lambda message: message.text == "Редагувати текст")
async def cmd_start(message: Message):
    if admin_log == True:
        await Form_text_a.text_slug.set()

        con = sqlite3.connect('main_text.db')
        c = con.cursor()
        with con:
            c.execute(f"SELECT * FROM text")
            rows = c.fetchall()
            for row in rows:
                await bot.send_message(chat_id=message.from_user.id, text=f"slug: {row[0]}\nTitle: {row[1]}")
            con.commit()
            c.close()
        await message.reply("Введите slug")
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


@dp.message_handler(state=Form_text_a.text_slug)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_slug'] = message.text

    con = sqlite3.connect('main_text.db')
    c = con.cursor()
    with con:
        c.execute(f"SELECT * FROM text WHERE text_slug = '{data['text_slug']}'")
        rows = c.fetchall()
        for row in rows:
            await bot.send_message(chat_id=message.from_user.id, text=f"{row[1]}\n\n{row[2]}",
                                   reply_markup=kb.admin_kb_text)
    con.commit()
    c.close()
    await Form_text_a.text_do.set()
    await message.reply("Що з ним робити?")


@dp.message_handler(state=Form_text_a.text_do)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_do'] = message.text
        await Form_text_a.text_new_s.set()
        await message.reply("На що міняємо?")


@dp.message_handler(state=Form_text_a.text_new_s)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_new_s'] = message.text
        if data['text_do'] == "Зміна title":
            con = sqlite3.connect('main_text.db')
            c = con.cursor()
            with con:
                c.execute(f"SELECT * FROM text")
                rows = c.fetchall()
                for row in rows:
                    c.execute(
                        f"UPDATE `text` SET `text_title` = '{data['text_new_s']}' WHERE text_slug = '{data['text_slug']}' ;")
            con.commit()
            c.close()
        if data['text_do'] == "Зміна text":
            con = sqlite3.connect('main_text.db')
            c = con.cursor()
            with con:
                c.execute(f"SELECT * FROM text")
                rows = c.fetchall()
                for row in rows:
                    c.execute(
                        f"UPDATE `text` SET `text_text` = '{data['text_new_s']}' WHERE text_slug = '{data['text_slug']}' ;")
            con.commit()
            c.close()
        await bot.send_message(chat_id=message.from_user.id, text=f"Готово!",
                               reply_markup=kb.admin_kb)
    await state.finish()


# КОНЕЦ Редактирование текстов

# Модерация отзывов

@dp.message_handler(lambda message: message.text == "Модерація відгуків")
async def cmd_start(message: Message):
    if admin_log == True:
        await bot.send_message(chat_id=message.from_user.id, text="Нові відгуки на модерацію")
        con = sqlite3.connect('review.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM review")
            rows = cur.fetchall()
            for row in rows:
                true_answer = "true_answer" + str(row[0])
                false_answer = "false_answer" + str(row[0])
                reviev_True = InlineKeyboardButton('True', callback_data=true_answer)
                reviev_False = InlineKeyboardButton('False', callback_data=false_answer)
                reviev_kb = InlineKeyboardMarkup().row(reviev_True, reviev_False)
                await bot.send_message(chat_id=message.from_user.id, text=f"{row[0]}\n{row[1]}\n{row[2]}",
                                       reply_markup=reviev_kb)
        con.commit()
        cur.close()
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")

    # КОНЕЦ Модерация отзывов

    #  Редактирование меню

@dp.message_handler(lambda message: message.text == "Назад в Адмін панель")
async def cmd_start(message: Message):
    if admin_log == True:
        await bot.send_message(chat_id=message.from_user.id, text="Ви знову в адмін панелі!", reply_markup=kb.admin_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")

@dp.message_handler(lambda message: message.text == "Повернутися в редагування меню")
async def cmd_start(message: Message):
    if admin_log == True:
        await bot.send_message(chat_id=message.from_user.id, text="Що ви хочете?", reply_markup=kb.admin_menu_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


@dp.message_handler(lambda message: message.text == "Редагуваті меню")
async def cmd_start(message: Message):
    if admin_log == True:
        await bot.send_message(chat_id=message.from_user.id, text="Що ви хочете?", reply_markup=kb.admin_menu_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


@dp.message_handler(lambda message: message.text == "Додавання")
async def cmd_start(message: Message):
    if admin_log == True:
        await bot.send_message(chat_id=message.from_user.id, text="Что вы хотите добавить?", reply_markup=kb.admin_menu_add_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


class Form_add_menu__main_cat(StatesGroup):
    New_cat_for_add_main_cat = State()
    New_sub_cat_for_add_main_cat = State()
    New_prod_articul_cat_for_add_main_cat = State()
    New_prod_name_cat_for_add_main_cat = State()
    New_prod_desc_cat_for_add_main_cat = State()
    New_prod_w_cat_for_add_main_cat = State()
    New_prod_price_cat_for_add_main_cat = State()
    New_prod_img_cat_for_add_main_cat = State()


@dp.message_handler(lambda message: message.text == "Додати основні категорії")
async def cmd_start(message: Message):
    if admin_log == True:
        await Form_add_menu__main_cat.New_cat_for_add_main_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text='Введіть основну категорію',
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


@dp.message_handler(state=Form_add_menu__main_cat.New_cat_for_add_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_cat_for_add_main_cat'] = message.text

        await Form_add_menu__main_cat.New_sub_cat_for_add_main_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text='Введіть підкатегорію', reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=Form_add_menu__main_cat.New_sub_cat_for_add_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_sub_cat_for_add_main_cat'] = message.text

        await Form_add_menu__main_cat.New_prod_articul_cat_for_add_main_cat.set()

        await message.reply("Введіть артикул страви")

@dp.message_handler(state=Form_add_menu__main_cat.New_prod_articul_cat_for_add_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_articul_cat_for_add_main_cat'] = message.text

        await Form_add_menu__main_cat.New_prod_name_cat_for_add_main_cat.set()

        await message.reply("Введіть назву страви")

@dp.message_handler(state=Form_add_menu__main_cat.New_prod_name_cat_for_add_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_name_cat_for_add_main_cat'] = message.text

        await Form_add_menu__main_cat.New_prod_desc_cat_for_add_main_cat.set()

        await message.reply("Введіть опис страви")

@dp.message_handler(state=Form_add_menu__main_cat.New_prod_desc_cat_for_add_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_desc_cat_for_add_main_cat'] = message.text

        await Form_add_menu__main_cat.New_prod_w_cat_for_add_main_cat.set()

        await message.reply("Введіть вагу в форматі 150.00 г.")

@dp.message_handler(state=Form_add_menu__main_cat.New_prod_w_cat_for_add_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_w_cat_for_add_main_cat'] = message.text

        await Form_add_menu__main_cat.New_prod_price_cat_for_add_main_cat.set()

        await message.reply("Введіть ціну в форматі 150.00 грн.")

@dp.message_handler(state=Form_add_menu__main_cat.New_prod_price_cat_for_add_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_price_cat_for_add_main_cat'] = message.text

        await Form_add_menu__main_cat.New_prod_img_cat_for_add_main_cat.set()

        await message.reply("Надішліть img")

@dp.message_handler(state=Form_add_menu__main_cat.New_prod_img_cat_for_add_main_cat, content_types=['photo'])
async def handle_docs_photo(message, state: FSMContext):
    await message.photo[-1].download('img/' + message.photo[-1].file_id + '.jpg')
    async with state.proxy() as data:
        data['New_prod_img_cat_for_add_main_cat'] = message.photo[-1].file_id
        con = sqlite3.connect('prod_test_db_1.db.db')
        cur = con.cursor()
        with con:
            cur.execute(f"INSERT INTO `prod` VALUES ('{data['New_cat_for_add_main_cat']}', '{data['New_sub_cat_for_add_main_cat']}', '{data['New_prod_articul_cat_for_add_main_cat']}', '{data['New_prod_name_cat_for_add_main_cat']}', '{data['New_prod_desc_cat_for_add_main_cat']}', '{data['New_prod_w_cat_for_add_main_cat']}', '{data['New_prod_price_cat_for_add_main_cat']}', '{data['New_prod_img_cat_for_add_main_cat']}')")
        con.commit()
        cur.close()
        await bot.send_message(chat_id=message.from_user.id, text='Все додано', reply_markup=kb.admin_menu_kb)
    await state.finish()



@dp.message_handler(lambda message: message.text == "Добавить подкатегории")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_add_menu__main_cat.New_cat_for_add_main_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


class Form_add_menu__current_food_cat(StatesGroup):
    New_cat_for_add_current_food_cat = State()
    New_sub_cat_for_add_current_food_cat = State()
    New_prod_articul_cat_for_add_current_food_cat = State()
    New_prod_name_cat_for_add_current_food_cat = State()
    New_prod_desc_cat_for_add_current_food_cat = State()
    New_prod_w_cat_for_add_current_food_cat = State()
    New_prod_price_cat_for_add_current_food_cat = State()
    New_prod_img_cat_for_add_current_food_cat = State()

@dp.message_handler(lambda message: message.text == "Додати конкретну страву")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_add_menu__current_food_cat.New_cat_for_add_current_food_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")



@dp.message_handler(state=Form_add_menu__current_food_cat.New_cat_for_add_current_food_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_cat_for_add_current_food_cat'] = message.text

        global sub_cat_kb
        sub_cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE main_cat = '{data['New_cat_for_add_current_food_cat']}' ")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[1])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                sub_cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_add_menu__current_food_cat.New_sub_cat_for_add_current_food_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Підкатегорію"), reply_markup=sub_cat_kb)

@dp.message_handler(state=Form_add_menu__current_food_cat.New_sub_cat_for_add_current_food_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_sub_cat_for_add_current_food_cat'] = message.text

        await Form_add_menu__current_food_cat.New_prod_articul_cat_for_add_current_food_cat.set()

        await bot.send_message(chat_id=message.from_user.id, text="Введіть артикул страви", reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=Form_add_menu__current_food_cat.New_prod_articul_cat_for_add_current_food_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_articul_cat_for_add_current_food_cat'] = message.text

        await Form_add_menu__current_food_cat.New_prod_name_cat_for_add_current_food_cat.set()

        await message.reply("Введіть назву страви")

@dp.message_handler(state=Form_add_menu__current_food_cat.New_prod_name_cat_for_add_current_food_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_name_cat_for_add_current_food_cat'] = message.text

        await Form_add_menu__current_food_cat.New_prod_desc_cat_for_add_current_food_cat.set()

        await message.reply("Введіть опис страви")

@dp.message_handler(state=Form_add_menu__current_food_cat.New_prod_desc_cat_for_add_current_food_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_desc_cat_for_add_current_food_cat'] = message.text

        await Form_add_menu__current_food_cat.New_prod_w_cat_for_add_current_food_cat.set()

        await message.reply("Введіть вагу в форматі 150.00 г.")

@dp.message_handler(state=Form_add_menu__current_food_cat.New_prod_w_cat_for_add_current_food_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_w_cat_for_add_current_food_cat'] = message.text

        await Form_add_menu__current_food_cat.New_prod_price_cat_for_add_current_food_cat.set()

        await message.reply("Введіть ціну в форматі 150.00 грн.")

@dp.message_handler(state=Form_add_menu__current_food_cat.New_prod_price_cat_for_add_current_food_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['New_prod_price_cat_for_add_current_food_cat'] = message.text

        await Form_add_menu__current_food_cat.New_prod_img_cat_for_add_current_food_cat.set()

        await message.reply("Надішліть img")

@dp.message_handler(state=Form_add_menu__current_food_cat.New_prod_img_cat_for_add_current_food_cat, content_types=['photo'])
async def handle_docs_photo(message, state: FSMContext):
    await message.photo[-1].download('img/' + message.photo[-1].file_id + '.jpg')
    async with state.proxy() as data:
        data['New_prod_img_cat_for_add_current_food_cat'] = message.photo[-1].file_id
        con = sqlite3.connect('prod_test_db_1.db.db')
        cur = con.cursor()
        with con:
            cur.execute(f"INSERT INTO `prod` VALUES ('{data['New_cat_for_add_current_food_cat']}', '{data['New_sub_cat_for_add_current_food_cat']}', '{data['New_prod_articul_cat_for_add_current_food_cat']}', '{data['New_prod_name_cat_for_add_current_food_cat']}', '{data['New_prod_desc_cat_for_add_current_food_cat']}', '{data['New_prod_w_cat_for_add_current_food_cat']}', '{data['New_prod_price_cat_for_add_current_food_cat']}', '{data['New_prod_img_cat_for_add_current_food_cat']}')")
        con.commit()
        cur.close()
        await bot.send_message(chat_id=message.from_user.id, text='Все додано')
    await state.finish()






@dp.message_handler(lambda message: message.text == "Редактирование")
async def cmd_start(message: Message):
    if admin_log == True:
        await bot.send_message(chat_id=message.from_user.id, text="Что вы хотите?", reply_markup=kb.admin_menu_red_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")



class Form_edit_main_cat(StatesGroup):
    edit_main_cat = State()
    edit_new_main_cat = State()

@dp.message_handler(lambda message: message.text == "Редагувати основні категорії")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_edit_main_cat.edit_main_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")

@dp.message_handler(state=Form_edit_main_cat.edit_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_main_cat'] = message.text
        await Form_edit_main_cat.edit_new_main_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text='Введіть нову назву',
                               reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state= Form_edit_main_cat.edit_new_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_new_main_cat'] = message.text

        con = sqlite3.connect('prod_test_db_1.db.db')
        cur = con.cursor()
        with con:
            cur.execute(f"UPDATE `prod` SET `main_cat` = '{data['edit_new_main_cat']}' WHERE main_cat = '{data['edit_main_cat']}';")
        con.commit()
        cur.close()

        await bot.send_message(chat_id=message.from_user.id, text='Готово!', reply_markup=kb.admin_menu_kb)
    await state.finish()




class Form_edit_sub_cat(StatesGroup):
    edit_main_cat_sub = State()
    edit_sub_cat_sub = State()
    edit_new_sub_cat = State()

@dp.message_handler(lambda message: message.text == "Редагувати підкатегорії")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_edit_sub_cat.edit_main_cat_sub.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")

@dp.message_handler(state=Form_edit_sub_cat.edit_main_cat_sub)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_main_cat_sub'] = message.text
        global subcat_kb
        subcat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE main_cat = '{data['edit_main_cat_sub']}'")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[1])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                subcat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_edit_sub_cat.edit_sub_cat_sub.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Підкатегорію"), reply_markup=subcat_kb)

@dp.message_handler(state=Form_edit_sub_cat.edit_sub_cat_sub)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_sub_cat_sub'] = message.text
        await Form_edit_sub_cat.edit_new_sub_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text='Введіть нову назву',
                               reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state= Form_edit_sub_cat.edit_new_sub_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_new_sub_cat'] = message.text

        con = sqlite3.connect('prod_test_db_1.db.db')
        cur = con.cursor()
        with con:
            cur.execute(f"UPDATE `prod` SET sub_cat = '{data['edit_new_sub_cat']}' WHERE sub_cat = '{data['edit_sub_cat_sub']}';")
        con.commit()
        cur.close()

        await bot.send_message(chat_id=message.from_user.id, text='Готово!', reply_markup=kb.admin_menu_kb)
    await state.finish()





class Form_edit_prod(StatesGroup):
    edit_main_prod = State()
    edit_sub_prod = State()
    edit_prod_for_edit = State()
    edit_prod_property_old = State()
    edit_prod_property_new = State()

@dp.message_handler(lambda message: message.text == "Редагувати конкретну страву")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_edit_prod.edit_main_prod.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")

@dp.message_handler(state=Form_edit_prod.edit_main_prod)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_main_prod'] = message.text
        global subcat_kb
        subcat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE main_cat = '{data['edit_main_prod']}'")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[1])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                subcat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_edit_prod.edit_sub_prod.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Підкатегорію"), reply_markup=subcat_kb)

@dp.message_handler(state=Form_edit_prod.edit_sub_prod)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_sub_prod'] = message.text
        global prod_kb
        prod_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE sub_cat = '{data['edit_sub_prod']}'")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[3])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                prod_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()

        await Form_edit_prod.edit_prod_for_edit.set()
        await bot.send_message(chat_id=message.from_user.id, text='Виберете блюдо для редагування',
                               reply_markup=prod_kb)

@dp.message_handler(state= Form_edit_prod.edit_prod_for_edit)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_prod_for_edit'] = message.text

        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE prod_name = '{data['edit_prod_for_edit']}'")
            rows = cur.fetchall()
            for row in rows:
                text_prod = str(row[2]) + '\n\n' + str(row[3]) + '\n\n' + str(row[4]) + '\n\n' + str(
                    row[5]) + '\n\n' + str(row[6])
                await bot.send_photo(chat_id=message.from_user.id,
                                     photo=row[7], caption=text_prod)
            con.commit()
            cur.close()
        await Form_edit_prod.edit_prod_property_old.set()
        await bot.send_message(chat_id=message.from_user.id, text='Що робити?', reply_markup=kb.admin_menu_edit_prod_kb)

@dp.message_handler(state=Form_edit_prod.edit_prod_property_old)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_prod_property_old'] = message.text
        await Form_edit_prod.edit_prod_property_new.set()
        await bot.send_message(chat_id=message.from_user.id, text='Введіть нове значення',
                               reply_markup=ReplyKeyboardRemove())

@dp.message_handler(state=Form_edit_prod.edit_prod_property_new, content_types=['photo'])
async def handle_docs_photo(message, state: FSMContext):
    await message.photo[-1].download('img/' + message.photo[-1].file_id + '.jpg')
    async with state.proxy() as data:
        data['edit_prod_property_new'] = message.photo[-1].file_id
        if data['edit_prod_property_old'] == 'Редагувати Фото':
            con = sqlite3.connect('prod_test_db_1.db.db')
            cur = con.cursor()
            with con:
                cur.execute(
                    f"UPDATE `prod` SET `prod_photo_id` = '{data['edit_prod_property_new']}' WHERE prod_name = '{data['edit_prod_for_edit']}';")
            con.commit()
            cur.close()

        await bot.send_message(chat_id=message.from_user.id, text='Готово!',
                               reply_markup=kb.admin_menu_kb)
    await state.finish()

@dp.message_handler(state=Form_edit_prod.edit_prod_property_new)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_prod_property_new'] = message.text
        if data['edit_prod_property_old'] == 'Редагувати Артикул':
            con = sqlite3.connect('prod_test_db_1.db.db')
            cur = con.cursor()
            with con:
                cur.execute(
                    f"UPDATE `prod` SET `prod_articul` = '{data['edit_prod_property_new']}' WHERE prod_name = '{data['edit_prod_for_edit']}';")
            con.commit()
            cur.close()
        if data['edit_prod_property_old'] == 'Редагувати Назву':

            con = sqlite3.connect('prod_test_db_1.db.db')
            cur = con.cursor()
            with con:
                cur.execute(
                    f"UPDATE `prod` SET `prod_name` = '{data['edit_prod_property_new']}' WHERE prod_name = '{data['edit_prod_for_edit']}';")
            con.commit()
            cur.close()
        if data['edit_prod_property_old'] == 'Редагувати Опис':

            con = sqlite3.connect('prod_test_db_1.db.db')
            cur = con.cursor()
            with con:
                cur.execute(
                    f"UPDATE `prod` SET `prod_desc` = '{data['edit_prod_property_new']}' WHERE prod_name = '{data['edit_prod_for_edit']}';")
            con.commit()
            cur.close()
        if data['edit_prod_property_old'] == 'Редагувати Вагу':

            con = sqlite3.connect('prod_test_db_1.db.db')
            cur = con.cursor()
            with con:
                cur.execute(
                    f"UPDATE `prod` SET `prod_w` = '{data['edit_prod_property_new']}' WHERE prod_name = '{data['edit_prod_for_edit']}';")
            con.commit()
            cur.close()
        if data['edit_prod_property_old'] == 'Редагувати Ціну':

            con = sqlite3.connect('prod_test_db_1.db.db')
            cur = con.cursor()
            with con:
                cur.execute(
                    f"UPDATE `prod` SET `prod_price` = '{data['edit_prod_property_new']}' WHERE prod_name = '{data['edit_prod_for_edit']}';")
            con.commit()
            cur.close()
        if data['edit_prod_property_old'] == 'Редагувати Фото':

            con = sqlite3.connect('prod_test_db_1.db.db')
            cur = con.cursor()
            with con:
                cur.execute(
                    f"UPDATE `prod` SET `prod_photo_id` = '{data['edit_prod_property_new']}' WHERE prod_name = '{data['edit_prod_for_edit']}';")
            con.commit()
            cur.close()

        await bot.send_message(chat_id=message.from_user.id, text='Готово!',
                               reply_markup=kb.admin_menu_kb)
    await state.finish()

@dp.message_handler(state=Form_add_menu__current_food_cat.New_prod_img_cat_for_add_current_food_cat, content_types=['photo'])
async def handle_docs_photo(message, state: FSMContext):
    await message.photo[-1].download('img/' + message.photo[-1].file_id + '.jpg')
    async with state.proxy() as data:
        data['New_prod_img_cat_for_add_current_food_cat'] = message.photo[-1].file_id







@dp.message_handler(lambda message: message.text == "Видалення")
async def cmd_start(message: Message):
    if admin_log == True:
        text = "Подсказка:\nПри удалении категории удалиться категория, подкатегории которые внутри этой категории а так-же все блюда\n При удалении подкатегории удалятся так-же все блюда внутри её"
        await bot.send_message(chat_id=message.from_user.id, text=text, reply_markup=kb.admin_menu_del_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")


class Form_remove_main_cat(StatesGroup):
    remove_main_cat = State()

@dp.message_handler(lambda message: message.text == "Видалити основні категорії")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_remove_main_cat.remove_main_cat.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")
@dp.message_handler(state= Form_remove_main_cat.remove_main_cat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['remove_main_cat'] = message.text

        con = sqlite3.connect('prod_test_db_1.db.db')
        cur = con.cursor()
        with con:
            cur.execute(f"DELETE FROM `prod` WHERE main_cat = '{data['remove_main_cat']}' ")
        con.commit()
        cur.close()

        await bot.send_message(chat_id=message.from_user.id, text='Ця категорія і все що в ній видалено', reply_markup=kb.admin_menu_kb)
    await state.finish()

class Form_remove_subcat(StatesGroup):
    remove_main_cat_for_subcat = State()
    remove_subcat_for_subcat = State()

@dp.message_handler(lambda message: message.text == "Видалити підкатегорії")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_remove_subcat.remove_main_cat_for_subcat.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")

@dp.message_handler(state=Form_remove_subcat.remove_main_cat_for_subcat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['remove_main_cat_for_subcat'] = message.text

        global subcat_kb
        subcat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE main_cat = '{data['remove_main_cat_for_subcat']}' ")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[1])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                subcat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_remove_subcat.remove_subcat_for_subcat.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете підкатегорії для видалення"), reply_markup=subcat_kb)

@dp.message_handler(state=Form_remove_subcat.remove_subcat_for_subcat)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['remove_subcat_for_subcat'] = message.text

        con = sqlite3.connect('prod_test_db_1.db.db')
        cur = con.cursor()
        with con:
            cur.execute(f"DELETE FROM `prod` WHERE sub_cat = '{data['remove_subcat_for_subcat']}' ")
        con.commit()
        cur.close()

        await bot.send_message(chat_id=message.from_user.id, text='Ця категорія і все що в ній видалено',
                               reply_markup=kb.admin_menu_kb)

    await state.finish()


class Form_remove_prod(StatesGroup):
    remove_main_cat_for_prod = State()
    remove_subcat_for_prod = State()
    remove_prod_for_prod = State()

@dp.message_handler(lambda message: message.text == "Видалити конкретну страву")
async def cmd_start(message: Message):
    if admin_log == True:
        global cat_kb
        cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[0])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_remove_prod.remove_main_cat_for_prod.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="У вас немає на це прав!")

@dp.message_handler(state=Form_remove_prod.remove_main_cat_for_prod)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['remove_main_cat_for_prod'] = message.text

        global subcat_kb
        subcat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE main_cat = '{data['remove_main_cat_for_prod']}' ")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[1])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                subcat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_remove_prod.remove_subcat_for_prod.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете підкатегорію"), reply_markup=subcat_kb)

@dp.message_handler(state=Form_remove_prod.remove_subcat_for_prod)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['remove_subcat_for_prod'] = message.text
        global prod_kb
        prod_kb = ReplyKeyboardMarkup(resize_keyboard=True)
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"SELECT * FROM prod WHERE sub_cat = '{data['remove_subcat_for_prod']}' ")
            rows = cur.fetchall()
            row_fix_cat = []
            for row in rows:
                row_fix_cat.append(row[3])
            new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
            counter_cat = 0

            for row in new_row_fix_cat:
                counter_cat += 1
                counter_cat_st = str(counter_cat)
                globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                prod_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        con.commit()
        cur.close()
        await Form_remove_prod.remove_prod_for_prod.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Виберете страву для видалення"),
                               reply_markup=prod_kb)

@dp.message_handler(state=Form_remove_prod.remove_prod_for_prod)
async def process_name_1(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['remove_prod_for_prod'] = message.text
        con = sql.connect('prod_test_db_1.db.db')
        with con:
            cur = con.cursor()
            cur.execute(f"DELETE FROM `prod` WHERE prod_name = '{data['remove_prod_for_prod']}' ")
        con.commit()
        cur.close()
        await Form_remove_prod.remove_prod_for_prod.set()
        await bot.send_message(chat_id=message.from_user.id, text=("Видалено"),
                               reply_markup=kb.admin_menu_kb)



    await state.finish()


#  КОНЕЦ Редактирование меню


@dp.callback_query_handler()
async def process_callback_button1(callback_query: CallbackQuery):
    if " Кошик: " in callback_query.data:
        s.append(callback_query.data)
        text = "Товар доданий!"
        await bot.send_message(callback_query.from_user.id, text=text, reply_markup=kb.greet_kb)
    if "true_answer" in callback_query.data:

        async def send_telegram(text: str):
            token = BOT_TOKEN
            url = "https://api.telegram.org/bot"
            channel_id = "@Resto_delivery_reviews"
            url += token
            method = url + "/sendMessage"

            r = requests.post(method, data={
                "chat_id": channel_id,
                "text": text
            })

        con = sqlite3.connect('review.db')
        with con:
            cur = con.cursor()

            review_id = callback_query.data.replace('true_answer', '')

            cur.execute(f"SELECT * FROM review WHERE id = '{review_id}'")
            rows = cur.fetchall()
            for row in rows:
                text_reviev_to_chat = (row[2] + '\n\n' + 'От: ' + row[1])
            cur.execute(f"DELETE FROM review WHERE id = '{review_id}'")
        con.commit()
        cur.close()
        await send_telegram(md.text(

            md.text(text_reviev_to_chat),

            sep='\n',

        ))
    if "false_answer" in callback_query.data:
        con = sqlite3.connect('review.db')
        with con:
            cur = con.cursor()
            review_id = callback_query.data.replace('false_answer', '')
            cur.execute(f"DELETE FROM review WHERE id = '{review_id}'")
        con.commit()
        cur.close()
        await bot.send_message(callback_query.from_user.id, text="Видалено!")

    if "Оплата" in callback_query.data:
        texta = callback_query.data.replace('Оплата', '')
        global order_id
        my_file = open("current_order.txt")
        my_string = my_file.read()
        order_id = 'cofeDoor' + my_string
        new_my_string = int(my_string) + int(1)
        my_file.close()

        my_file = open("current_order.txt", "w")
        my_file.write(str(new_my_string))
        my_file.close()

        data = {
                    "order_id": order_id,
                    "currency": "UAH",
                    "amount": texta,
        }

        url = checkout.url(data).get('checkout_url')

        await bot.send_message(callback_query.from_user.id, text=url)
        for _ in range(30):

            url = 'https://api.fondy.eu/api/status/order_id'
            headers = {'Content-type': 'application/json',  # Определение типа данных
                       'Accept': 'text/plain',
                       'Content-Encoding': 'utf-8'}
            to_sha1 = "test|1396424|" + order_id
            to_sha1 = bytes(to_sha1, 'utf-8')
            hash_object = hashlib.sha1(to_sha1)
            hex_dig = hash_object.hexdigest()

            data = {
                "request": {
                    "order_id": order_id,
                    "signature": hex_dig,
                    "merchant_id": "1396424"
                }

            }

            answer = requests.post(url, data=json.dumps(data), headers=headers)
            response = answer.json()
            if "'order_status': 'approved'" in str(response):
                print("Оплата завершена!")

                async def send_telegram(text: str):
                    token = BOT_TOKEN
                    url = "https://api.telegram.org/bot"
                    channel_id = "@Resto_delivery_order"
                    url += token
                    method = url + "/sendMessage"

                    r = requests.post(method, data={
                        "chat_id": channel_id,
                        "text": text
                    })
                text_to_pay = ''
                for card_cart in s:
                    card_cart = card_cart.replace('Кошик: ', '')
                    con = sql.connect('prod_test_db_1.db.db')
                    with con:
                        cur = con.cursor()
                        cur.execute(f"SELECT * FROM prod WHERE prod_articul ='{card_cart}' ")
                        rows = cur.fetchall()
                        for row in rows:
                            text_prod = str(row[2]) + ' ' + str(row[3]) + ' ' + str(row[4]) + ' ' + str(row[5]) + '\n\n'
                            text_to_pay = str(text_to_pay) + str(text_prod)
                        con.commit()
                        cur.close()
                await send_telegram(md.text(

                    md.text(text_to_pay),
                    md.text('Оплата за безготівковим розрахунком'),

                    sep='\n',

                ))

                break
            time.sleep(10 - time.time() % 10)




# Начинаем наш диалог
@dp.message_handler(lambda message: message.text == "Доставка" or 'Назад в меню' )
async def cmd_start(message: Message):
    global cat_kb
    button_7 = KeyboardButton('Кошик')
    button_8 = KeyboardButton('В головне меню')
    cat_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_7)
    con = sql.connect('prod_test_db_1.db.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM prod")
        rows = cur.fetchall()
        row_fix_cat = []
        for row in rows:
            row_fix_cat.append(row[0])
        row_fix_cat.sort()
        new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
        counter_cat = 0

        for row in new_row_fix_cat:
            counter_cat += 1
            counter_cat_st = str(counter_cat)
            globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
            cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
        cat_kb.row(button_8)
    con.commit()
    cur.close()
    await Form_prod.cat.set()
    await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)


# Сюда приходит ответ с именем
@dp.message_handler(state=Form_prod.cat)
async def process_cat(message: Message, state: FSMContext):
    sub_cat_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    async with state.proxy() as data:
        data['cat'] = message.text
    con = sql.connect('prod_test_db_1.db.db')
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM prod WHERE main_cat = '{data['cat']}'")
        rows = cur.fetchall()
        row_fix_cat = []
        for row in rows:
            row_fix_cat.append(row[1])
        row_fix_cat.sort()
        new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
        counter_sub_cat = 0
        for row in new_row_fix_cat:
            counter_sub_cat += 1
            counter_sub_cat_st = str(counter_sub_cat)
            globals()[str('buttonmenucat_%s') + str(counter_sub_cat_st)] = KeyboardButton(f"{str(row)}")
            sub_cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_sub_cat_st)])
    con.commit()
    cur.close()
    if data['cat'] == 'В головне меню':
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id, text=("Вы снова в меню!"), reply_markup=kb.greet_kb)
    elif data['cat'] == 'Кошик':
        await state.finish()
        global total
        total = 0
        for card_cart in s:
            card_cart = card_cart.replace('Кошик: ', '')
            con = sql.connect('prod_test_db_1.db.db')
            with con:
                cur = con.cursor()
                cur.execute(f"SELECT * FROM prod WHERE prod_articul ='{card_cart}' ")
                rows = cur.fetchall()
                for row in rows:
                    prod_price = float(row[6].replace(' грн', '').replace("'", ""))
                    total = total + prod_price
                    text_prod = str(row[2]) + '\n\n' + str(row[3]) + '\n\n' + str(row[4]) + '\n\n' + str(row[5])
                    await bot.send_photo(chat_id=message.from_user.id,
                                         photo=row[7], caption=text_prod)
                con.commit()
                cur.close()
        To_cart_btn = KeyboardButton('Оформить заказ')
        To_cat_btn = KeyboardButton('Назад в меню')
        To_cart_kb = ReplyKeyboardMarkup().row(To_cart_btn).row(To_cat_btn)

        await Form_cart_to_pay.total_sum.set()
        total_text = 'Загальна сума замовлення: ' + str(total) + ' грн'
        if total == 0:
            total_text = 'Ваш кошик порожній!'
        await bot.send_message(chat_id=message.from_user.id, text=total_text, reply_markup=To_cart_kb)

    else:
        button_8 = KeyboardButton('В головне меню')
        await Form_prod.next()
        sub_cat_kb.row(button_8)
        await bot.send_message(chat_id=message.from_user.id, text=("Под категория"), reply_markup=sub_cat_kb)


# Сохраняем пол, выводим анкету
@dp.message_handler(state=Form_prod.sub_cat)
async def process_sub_cat(message: Message, state: FSMContext):
    if data['cat'] == 'В головне меню':
        await state.finish()
        await bot.send_message(chat_id=message.from_user.id, text=("Вы снова в меню!"), reply_markup=kb.greet_kb)
    else :
        async with state.proxy() as data:
            data['sub_cat'] = message.text
            con = sql.connect('prod_test_db_1.db.db')
            with con:
                cur = con.cursor()
                cur.execute(f"SELECT * FROM prod WHERE main_cat = '{data['cat']}' AND sub_cat ='{data['sub_cat']}' ")
                rows = cur.fetchall()
                for row in rows:
                    text_prod =  str(row[3]) + '\n\n' + str(row[4]) + '\n\n' + str(row[5]) + '\n\n' + str(row[6])
                    data_prod = ' Кошик: ' + str(row[2])
                    inline_btn_1 = InlineKeyboardButton(text='Додати в кошик!', callback_data=data_prod)
                    inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)
                    await bot.send_photo(chat_id=message.from_user.id,
                                        photo=row[7], caption=text_prod, reply_markup=inline_kb1)
                con.commit()
                cur.close()
                await bot.send_message(chat_id=message.from_user.id, text=("Вы знову в меню!"), reply_markup=kb.greet_kb)
        await state.finish()


class Form_cart_to_pay(StatesGroup):
    total_sum = State()
    tel_to_pay = State()
    address_to_pay = State()
    comment_to_order = State()
    var_pay = State()

# Сюда приходит ответ с именем
@dp.message_handler(state=Form_cart_to_pay.total_sum)
async def process_cat(message: Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Назад в меню':
            global cat_kb
            button_7 = KeyboardButton('Кошик')
            button_8 = KeyboardButton('В головне меню')
            cat_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(button_7)
            con = sql.connect('prod_test_db_1.db.db')
            with con:
                cur = con.cursor()
                cur.execute(f"SELECT * FROM prod")
                rows = cur.fetchall()
                row_fix_cat = []
                for row in rows:
                    row_fix_cat.append(row[0])
                row_fix_cat.sort()
                new_row_fix_cat = [el for el, _ in groupby(row_fix_cat)]
                counter_cat = 0

                for row in new_row_fix_cat:
                    counter_cat += 1
                    counter_cat_st = str(counter_cat)
                    globals()[str('buttonmenucat_%s') + str(counter_cat_st)] = KeyboardButton(f"{str(row)}")
                    cat_kb.row(globals()[str('buttonmenucat_%s') + str(counter_cat_st)])
                cat_kb.row(button_8)
            con.commit()
            cur.close()
            await Form_prod.cat.set()
            await bot.send_message(chat_id=message.from_user.id, text=("Виберете Категорію"), reply_markup=cat_kb)
            await state.finish()
        else:
            data['total_sum'] = total * 100
            await bot.send_message(chat_id=message.from_user.id, text='Введіть ваш контактний номер телефону', reply_markup=ReplyKeyboardRemove() )
            await Form_cart_to_pay.tel_to_pay.set()

@dp.message_handler(state=Form_cart_to_pay.tel_to_pay)
async def process_cat(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['tel_to_pay'] = message.text
        await bot.send_message(chat_id=message.from_user.id, text='Введіть Адресу доставки', reply_markup=ReplyKeyboardRemove() )
        await Form_cart_to_pay.address_to_pay.set()

@dp.message_handler(state=Form_cart_to_pay.address_to_pay)
async def process_cat(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['address_to_pay'] = message.text
        await bot.send_message(chat_id=message.from_user.id, text='Введіть Коментар до замовлення', reply_markup=ReplyKeyboardRemove() )
        await Form_cart_to_pay.comment_to_order.set()

@dp.message_handler(state=Form_cart_to_pay.comment_to_order)
async def process_cat(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['comment_to_order'] = message.text
        await bot.send_message(chat_id=message.from_user.id, text='Спосіб оплати', reply_markup=kb.var_to_pay_kb )
        await Form_cart_to_pay.var_pay.set()

@dp.message_handler(state=Form_cart_to_pay.var_pay)
async def process_cat(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['var_pay'] = message.text
        tel_to_pay = data['tel_to_pay']
        address_to_pay = data['address_to_pay']
        comment_to_order = data['comment_to_order']
        if data['var_pay'] == 'Готівкова оплата при доставці':
            async def send_telegram(text: str):
                token = BOT_TOKEN
                url = "https://api.telegram.org/bot"
                channel_id = "@Resto_delivery_order"
                url += token
                method = url + "/sendMessage"

                r = requests.post(method, data={
                    "chat_id": channel_id,
                    "text": text
                })

            texta = data['total_sum']
            texta = texta / 100
            text_to_pay = ''
            for card_cart in s:
                card_cart = card_cart.replace('Кошик: ', '')
                con = sql.connect('prod_test_db_1.db.db')
                with con:
                    cur = con.cursor()
                    cur.execute(f"SELECT * FROM prod WHERE prod_articul ='{card_cart}' ")
                    rows = cur.fetchall()
                    for row in rows:
                        text_prod = str(row[2]) + ' ' + str(row[3]) + ' ' + str(row[4]) + ' ' + str(
                            row[5]) + '\n\n'
                        text_to_pay = str(text_to_pay) + str(text_prod)
                    con.commit()
                    cur.close()
            await send_telegram(md.text(

                md.text(text_to_pay),
                md.text('Загальна сума замовлення: ' + str(texta) + '\n'),
                md.text('Контактний номер телефону: ' + data['tel_to_pay'] + '\n'),
                md.text('Адреса доставки: ' + data['address_to_pay'] + '\n'),
                md.text('Коментар до замовлення: ' + data['comment_to_order'] + '\n'),
                md.text('Оплата при доставці '),

                sep='\n',

            ))

            await bot.send_message(chat_id=message.from_user.id, text='З вами зв`яжеться менеджер для уточнення замовлення, чекайте', reply_markup=kb.greet_kb)
        if data['var_pay'] == 'Безготівкова оплата':

            texta = data['total_sum']
            global order_id
            my_file = open("current_order.txt")
            my_string = my_file.read()
            order_id = 'cofeDoor' + my_string
            new_my_string = int(my_string) + int(1)
            my_file.close()

            my_file = open("current_order.txt", "w")
            my_file.write(str(new_my_string))
            my_file.close()

            data = {
                "order_id": order_id,
                "currency": "UAH",
                "amount": int(texta)
            }

            url = checkout.url(data).get('checkout_url')
            await bot.send_message(chat_id=message.from_user.id, text='Будь ласка, проведіть оплату протягом 5 хвилин', reply_markup=ReplyKeyboardRemove())
            await bot.send_message(chat_id=message.from_user.id, text=url)
            for _ in range(30):

                url = 'https://api.fondy.eu/api/status/order_id'
                headers = {'Content-type': 'application/json',  # Определение типа данных
                           'Accept': 'text/plain',
                           'Content-Encoding': 'utf-8'}
                to_sha1 = "test|1396424|" + order_id
                to_sha1 = bytes(to_sha1, 'utf-8')
                hash_object = hashlib.sha1(to_sha1)
                hex_dig = hash_object.hexdigest()

                data = {
                    "request": {
                        "order_id": order_id,
                        "signature": hex_dig,
                        "merchant_id": "1396424"
                    }
                }

                answer = requests.post(url, data=json.dumps(data), headers=headers)
                response = answer.json()
                if "'order_status': 'approved'" in str(response):
                    await bot.send_message(chat_id=message.from_user.id, text='Оплата проведена! \n З вами зв`яжеться менеджер для уточнення', reply_markup=kb.greet_kb)

                    async def send_telegram(text: str):
                        token = BOT_TOKEN
                        url = "https://api.telegram.org/bot"
                        channel_id = "@Resto_delivery_order"
                        url += token
                        method = url + "/sendMessage"

                        r = requests.post(method, data={
                            "chat_id": channel_id,
                            "text": text
                        })

                    text_to_pay = ''
                    texta = texta / 100
                    for card_cart in s:
                        card_cart = card_cart.replace('Кошик: ', '')
                        con = sql.connect('prod_test_db_1.db.db')
                        with con:
                            cur = con.cursor()
                            cur.execute(f"SELECT * FROM prod WHERE prod_articul ='{card_cart}' ")
                            rows = cur.fetchall()
                            for row in rows:
                                text_prod = str(row[2]) + ' ' + str(row[3]) + ' ' + str(row[4]) + ' ' + str(
                                    row[5]) + '\n\n'
                                text_to_pay = str(text_to_pay) + str(text_prod)
                            con.commit()
                            cur.close()
                    await send_telegram(md.text(

                        md.text(text_to_pay),
                        md.text('Загальна сума замовлення:' + str(texta) + '\n'),
                        md.text('Контактний номер телефону:' + str(tel_to_pay)  + '\n'),
                        md.text('Адреса доставки:' + str(address_to_pay)  + '\n'),
                        md.text('Коментар до замовлення' +  str(comment_to_order) + '\n'),
                        md.text('Оплата по безналу'),

                        sep='\n',

                    ))

                    break
                time.sleep(10 - time.time() % 10)

    await state.finish()


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message):
    await message.photo[-1].download('img/' + message.photo[-1].file_id + '.jpg')
    text = message.photo[-1].file_id
    await bot.send_message(chat_id=message.from_user.id, text=text)


@dp.message_handler(lambda message: message.text == "Фото")
async def ask(message: Message):
    await bot.send_photo(chat_id=message.from_user.id,
                         photo="AgACAgIAAxkBAAIE0F_M2G6yq7vreAvkQbPsy0NBAAEucAACv7AxG1ybaEo44q35M9wNPCo5R5guAAMBAAMCAAN5AAOZ_gMAAR4E")





import telebot
from telebot import types
import sqlite3
import hashlib
import requests
from datetime import datetime

BITRIX_CRM_API_URL_1 = "https://b24-rolvpq.bitrix24.ru/rest/1/dxte8zsvvzvusx97/crm.lead.add.json" #добавление лида
BITRIX_CRM_API_URL_2 = "https://b24-rolvpq.bitrix24.ru/rest/1/dxte8zsvvzvusx97/crm.product.add.json" #добавление продукта
BITRIX_CRM_API_URL_3 = "https://b24-rolvpq.bitrix24.ru/rest/1/dxte8zsvvzvusx97/crm.contact.add.json" #добавление контакта
bot = telebot.TeleBot('6929738714:AAFf7yFYP01bVibY8FBs9obyQYBaZfOGe48')  # коннект с ботом @LevisSupportBot

name = None  # создание глобальных переменных
password = None
support_name = None
user_id = None
text = None
order_list = None
user_name = None
current_datetime = None
user_states = None


def create_lead(name, phone, email): # Функция для создания лида/сделки в CRM Bitrix
    data = {
        "fields": {
            "TITLE": "Новый лид от чат-бота Levi's",
            "NAME": name,
            "COMMENTS": order_list,
            # "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
            # "EMAIL": [{"VALUE": email, "VALUE_TYPE": "WORK"}]
        }
    }
    response = requests.post(BITRIX_CRM_API_URL_1, json=data)
    if response.status_code == 200:
        return "Товар успешно добавлен в корзину, в ближайшее время с Вами свяжется менеджер для уточнения информации и оплаты"
    else:
        return f"Произошла ошибка при создании лида: {response.text}"


def create_product(order_list): # Функция для создания продукта в CRM Bitrix
    data = {
        "fields": {
            "NAME": order_list,
            "CURRENCY_ID": "RUB",

        }
    }
    response = requests.post(BITRIX_CRM_API_URL_2, json=data)
    if response.status_code == 200:
        return "Продукт успешно добавлен в CRM Битрикс"
    else:
        return f"Произошла ошибка при добавлении товара: {response.text}"



def create_contact(name, current_datetime): # Функция для создания контакта в CRM Bitrix
    data = {
        "fields": {
            "NAME": name,
            "TYPE_ID": "CLIENT",
            "DATE_CREATE": current_datetime.isoformat(),
        }
    }
    response = requests.post(BITRIX_CRM_API_URL_3, json=data)
    if response.status_code == 200:
        return "Контакт успешно добавлен"
    else:
        return f"Произошла ошибка при добавлении контакта: {response.text}"



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton('🔐Регистрация')
    btn2 = types.KeyboardButton('👥О нас')
    btn3 = types.KeyboardButton('📦Товары')
    btn4 = types.KeyboardButton('🚀Заказ')
    btn5 = types.KeyboardButton('🆘Помощь')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, 'Привет, я помощник компании Levis!' + '\n' + 'Выберите, что Вас интересует: ', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def main_menu(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton('🔐Регистрация')
    btn2 = types.KeyboardButton('👥О нас')
    btn3 = types.KeyboardButton('📦Товары')
    btn4 = types.KeyboardButton('🚀Заказ')
    btn5 = types.KeyboardButton('🆘Помощь')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id, 'Выберите, что Вас интересует: ', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)



def on_click(message):
    if message.text == '🔐Регистрация':
        bot.send_message(message.chat.id, 'Хорошо, давайте я Вас зарегистрирую!' + '\n' + 'Введите Ваше имя')
        bot.register_next_step_handler(message, registration)
    elif message.text == '👥О нас':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton('↪️Вернуться в главное меню')
        markup.add(btn1)
        bot.send_message(message.chat.id, 'Мы дружная компания Levis!\n' + 'Мы любим изготавливать и продавать одежду', reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif message.text == '📦Товары':
        goods(message)
    elif message.text == '🚀Заказ':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton('✅Да')
        btn2 = types.KeyboardButton('❌Нет')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, 'Вы хотите сделать заказ?', reply_markup=markup)
        bot.register_next_step_handler(message, to_order)
    elif message.text == '🆘Помощь':
        bot.send_message(message.chat.id, 'Выберите по какой теме Вам нужна консультация ')
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton('🤔Как зарегистрироваться?')
        btn2 = types.KeyboardButton('🤔Как посмотреть товары?')
        btn3 = types.KeyboardButton('🤔Как сделать заказ?')
        btn4 = types.KeyboardButton('🤓Поговорить с человеком')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.chat.id, 'Вот темы, по которым я могу проконсультировать: ', reply_markup=markup)
        bot.register_next_step_handler(message, help)



def help(message):
    if message.text == '🤔Как зарегистрироваться?':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton('Основное меню')
        markup.add(btn1)
        bot.send_message(message.chat.id, 'Перейдите в основное меню и нажмите кнопку Регистрация', reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif message.text == '🤔Как посмотреть товары?':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton('Основное меню')
        markup.add(btn1)
        bot.send_message(message.chat.id, 'Перейдите в основное меню и нажмите кнопку Товары', reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif message.text == '🤔Как сделать заказ?':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        btn1 = types.KeyboardButton('Основное меню')
        markup.add(btn1)
        bot.send_message(message.chat.id, 'Перейдите в основное меню и нажмите кнопку Заказ', reply_markup=markup)
        bot.register_next_step_handler(message, main_menu)
    elif message.text == '🤓Поговорить с человеком':
        bot.send_message(message.chat.id, 'Давай я зарегистрирую Ваше обращение и направлю в нашу техподдержку\n' + 'Вам перезвонит наш помощник в ближайшее время\n' + 'Введите Ваше имя:')
        bot.register_next_step_handler(message, support)
    else:
        bot.send_message(message.chat.id, 'Такой темы нет')
        main_menu(message)



def registration(message):
    global name
    name = message.text.strip()
    if not name:
        bot.send_message(message.chat.id, 'Имя не может быть пустым. Пожалуйста, введите Ваше имя:')
        bot.register_next_step_handler(message, registration)
    else:
        bot.send_message(message.chat.id, 'Введите пароль. Не беспокойтесь, он будет зашифрован и никто не узнает Ваш пароль')
        bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    global name, password, current_datetime
    password = message.text.strip()
    if len(password) < 6:
        bot.send_message(message.chat.id, 'Пароль должен быть не менее 6 символов. Пожалуйста, введите пароль:')
        bot.register_next_step_handler(message, user_pass)
    else:
        hash_object = hashlib.md5(password.encode())
        conn = sqlite3.connect('levis.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, password TEXT)')
        cur.execute("INSERT INTO users (name, password) VALUES (?, ?)", (name, hash_object.hexdigest()))
        conn.commit()
        cur.close()
        conn.close()

        current_datetime = datetime.now()
        response = create_contact(name, current_datetime)
        bot.send_message(message.chat.id, response)
        bot.send_message(message.chat.id, 'Вы зарегистрированы!')
        main_menu(message)



def goods(message):
    conn = sqlite3.connect('levis.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM goods')
    goods = cur.fetchall()
    info = ''
    for el in goods:
        info += f'{el[1]} - {el[2]} рублей\n'
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Полный список наших товаров:\n' + info)

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton('✅Да')
    btn2 = types.KeyboardButton('❌Нет')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Хотите что-нибудь заказать?", reply_markup=markup)
    bot.register_next_step_handler(message, process_goods_response)


def process_goods_response(message):
    if message.text == '✅Да':
        bot.send_message(message.chat.id, 'Введите товары, которые хотите приобрести, в следующем виде:\nботинки\nкуртка')
        bot.register_next_step_handler(message, process_order)
    elif message.text == '❌Нет':
        bot.send_message(message.chat.id, 'Хорошо, давай вернёмся в главное меню')
        main_menu(message)
    else:
        bot.send_message(message.chat.id, 'Пожалуйста, выберите "Да" или "Нет"')
        bot.register_next_step_handler(message, process_goods_response)


def to_order(message):
    if message.text == '✅Да':
        bot.send_message(message.chat.id,'Введите товары, которые хотите приобрести, в следующем виде:\nботинки\nкуртка')
        bot.register_next_step_handler(message, process_order)
    elif message.text == '❌Нет':
        bot.send_message(message.chat.id, 'Хорошо, давай вернёмся в главное меню')
        main_menu(message)

def process_order(message):
    global order_list, user_name
    order_list = message.text.strip()
    user_name = message.chat.first_name if message.chat.first_name else "Пользователь"
    if not order_list:
        bot.send_message(message.chat.id, 'Список заказов не может быть пустым. Пожалуйста, введите товары:')
        bot.register_next_step_handler(message, process_order)
    else:
        conn = sqlite3.connect('levis.sql')
        cur = conn.cursor()
        cur.execute('SELECT name FROM goods')
        available_goods = [item[0].lower() for item in cur.fetchall()]

        # Проверяем, все ли введенные пользователем товары есть в списке доступных товаров
        ordered_goods = [item.strip().lower() for item in order_list.split('\n')]
        invalid_goods = [item for item in ordered_goods if item not in available_goods]

        if invalid_goods:
            bot.send_message(message.chat.id,f'Следующих товаров нет в наличии: {", ".join(invalid_goods)}. Пожалуйста, введите существующие товары:')
            goods(message)


        else:
            user_id = message.chat.id
            cur.execute('CREATE TABLE IF NOT EXISTS to_order (id INTEGER PRIMARY KEY AUTOINCREMENT, order_list TEXT, user_id TEXT)')
            cur.execute("INSERT INTO to_order (order_list, user_id) VALUES (?, ?)", (order_list, user_id))
            conn.commit()
            cur.close()
            conn.close()
            response = create_lead(user_name, user_id, order_list)
            bot.send_message(message.chat.id, response)
            order_choose(message)

def order_choose(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    btn1 = types.KeyboardButton('🗑Посмотреть мою корзину')
    btn2 = types.KeyboardButton('🔙Вернуться в меню')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Хотите посмотреть свою корзину или вернуться в главное меню?', reply_markup=markup)
    bot.register_next_step_handler(message, process_order_choose)


def process_order_choose(message):
    if message.text == '🗑Посмотреть мою корзину':
        basket_list(message)
    if message.text == '🔙Вернуться в меню':
        main_menu(message)



def basket_list(message):
    id = message.chat.id

    conn = sqlite3.connect('levis.sql')
    cur = conn.cursor()
    cur.execute('SELECT order_list FROM to_order WHERE user_id = ?', (id,))
    to_order = cur.fetchall()

    basket = ''
    for el in to_order:
        basket += f'{el[0]}\n'
    cur.close()
    conn.close()

    if len(basket) > 0:
        bot.send_message(message.chat.id, 'Ваша корзина:\n' + basket)
        main_menu(message)




def support(message):
    global support_name, user_id
    support_name = message.text.strip()
    if not support_name:
        bot.send_message(message.chat.id, 'Имя не может быть пустым. Пожалуйста, введите Ваше имя:')
        bot.register_next_step_handler(message, support)
    else:
        user_id = message.chat.id
        bot.send_message(message.chat.id, 'Кратко опишите Вашу проблему, пожалуйста')
        bot.register_next_step_handler(message, support_final)


def support_final(message):
    global support_name, text
    text = message.text.strip()
    if not text:
        bot.send_message(message.chat.id, 'Описание проблемы не может быть пустым. Пожалуйста, опишите Вашу проблему:')
        bot.register_next_step_handler(message, support_final)
    else:
        user_id = message.chat.id
        conn = sqlite3.connect('levis.sql')
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS help_request (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, user_id TEXT, text TEXT)')
        cur.execute("INSERT INTO help_request (name, user_id, text) VALUES (?, ?, ?)", (support_name, user_id, text))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, 'Спасибо за обращение, с Вами скоро свяжется наш менеджер!')
        main_menu(message)


bot.polling(none_stop=True)
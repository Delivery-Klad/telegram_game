from datetime import datetime
from telebot import types
import threading
import functions
import loopWork
import sqlite3
import telebot
import random
import time
import os

bot = telebot.TeleBot('1074352529:AAEIKKcGDpFtQt-7NNm0EYnxZiau9oARZAo')
delimiter_line = '------------------------------------------------'
databaseName = 'DataBase.db'
helpButtonName = 'Помощь🆘'
filesFolderName = 'files/'
logFileName = 'LogBot.txt'
acceptWorkButton = 'Выполнить работу'
cancelWorkButton = 'Отказаться'
print(bot.get_me())


@bot.message_handler(commands=['start'])
def handler_start(message):
    try:
        functions.log(message)
        functions.createTables()
        contain = False
        connect = sqlite3.connect(filesFolderName + databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID FROM Users")
        res = cursor.fetchall()
        for i in range(len(res)):
            if res[i][0] == message.from_user.id:
                contain = True
                break
        if not contain:
            data = [message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?)', data)
        connect.commit()
        if functions.notInLists(message):
            key1 = types.InlineKeyboardMarkup()
            key1.add(types.InlineKeyboardButton(text=helpButtonName, callback_data='0'))
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Welcome</b>')
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Узнать как пользоваться ботом</b>', reply_markup=key1)
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Вы что-то делаете...</b>')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['log'])  # функция обработки запроса логов
def handler_log(message):
    try:
        functions.log(message)
        if functions.isAdmin(message.from_user.id):
            doc = open(filesFolderName + logFileName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['db'])  # функция обработки запроса базы данных
def handler_db(message):
    try:
        functions.log(message)
        if functions.isAdmin(message.from_user.id):
            doc = open(filesFolderName + databaseName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['help'])  # обработка команды помощи
def handler_help(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='Меню помощи\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-')
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda c: True)  # функция обработки inline кнопок
def func(c):
    try:
        if c.data == '0':
            handler_help(c)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])  # функция обработки текстовых сообщений
def handler_text(message):
    try:
        if message.text == acceptWorkButton:
            o = 0
        elif message.text == cancelWorkButton:
            o = 0
        elif message.text == helpButtonName:
            o = 0
    except Exception as e:
        print(e)


try:  # максимально странная конструкция
    while True:
        t = threading.Thread(target=loopWork.timer, name='timer', args=[bot])
        t.start()
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(e)
except Exception as e:
    print(e)

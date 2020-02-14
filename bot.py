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

techList = ['программист', 'математик']
gumList = ['Миша', 'ленивая жопа']
print(bot.get_me())


@bot.message_handler(commands=['start'])
def handler_start(message):
    try:
        functions.log(message)
        functions.createTables()
        key1 = types.InlineKeyboardMarkup()
        key1.add(types.InlineKeyboardButton(text=helpButtonName, callback_data='0'))
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Welcome</b>')
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Узнать как пользоваться ботом</b>',
                         reply_markup=key1)
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
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>Для того, чтобы определить ваш '
                                                                                   'склад ума, скажите чему '
                                                                                   'равно</i> <b>2+2*2</b>')
            data = [message.from_user.id, message.from_user.username, "None", "None", "None",
                    str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?)', data)
        connect.commit()
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
        functions.log(message)
        connect = sqlite3.connect(filesFolderName + databaseName)
        cursor = connect.cursor()
        if message.text == acceptWorkButton or message.text == cancelWorkButton:
            o = 0
        elif message.text == helpButtonName:
            o = 0
        elif message.text in techList or message.text in gumList:
            if message.text in techList:
                cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
                spec = cursor.fetchall()
                if spec[0][0] == 'tech':
                    cursor.execute(
                        "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text), str(message.from_user.id)))
            else:
                cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
                spec = cursor.fetchall()
                if spec[0][0] == 'gum':
                    cursor.execute(
                        "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text), str(message.from_user.id)))
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<i>Ваша профессия ' + message.text + '</i>')
            connect.commit()
        else:
            cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
            spec = cursor.fetchall()
            if spec[0][0] == 'None':
                if message.text == "6":
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>Поздравляем, вы-технарь</b>')
                    cursor.execute("UPDATE Users SET Spec='tech' WHERE ID=" + str(message.from_user.id))
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row(techList[0], techList[1])
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь вы можете выбрать одну из предложенных профессий</i>',
                                     reply_markup=user_markup)
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>Соболезнуем, вы-гуманитарий</b>')
                    cursor.execute("UPDATE Users SET Spec='gum' WHERE ID=" + str(message.from_user.id))
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row(gumList[0], gumList[1])
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь вы можете выбрать одну из предложенных профессий</i>',
                                     reply_markup=user_markup)
                connect.commit()

        cursor.close()
        connect.close()
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

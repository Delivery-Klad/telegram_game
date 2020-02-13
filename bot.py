from datetime import datetime
from telebot import types
import threading
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


def log(message): # запись лога сообщений
    try:
        file = open(filesFolderName + logFileName, 'a')
        file.write('\n' + delimiter_line + '\n')
        file.write(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        if message.from_user.username != 'None' and message.from_user.username is not None:
            file.write('\nСообщение от {0}, (id = {1})\nТекст - {2}'.format(message.from_user.username,
                                                                            str(message.from_user.id),
                                                                            message.text))
        else:
            file.write('\nСообщение от {0} {1}, (id = {2})\nТекст - {3}'.format(message.from_user.first_name,
                                                                            message.from_user.last_name,
                                                                            str(message.from_user.id),
                                                                            message.text))
        print('\n' + delimiter_line)
        print(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        print('Сообщение от {0}, (id = {1})\nТекст - {2}'.format(message.from_user.username,
                                                                    str(message.from_user.id),
                                                                    message.text))
        file.close()
    except Exception as e:
        print(e)


def createTables(): # создание таблиц в sql если их нет
    try:
        connect = sqlite3.connect(filesFolderName + databaseName)
        cursor = connect.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Admins(ID INTEGER,'
                        'UserName TEXT,'
                        'First_Name TEXT,'
                        'Last_Name TEXT,'
                        'Permissions INTEGER)')
        cursor.execute('CREATE TABLE IF NOT EXISTS Users(ID INTEGER,'
                        'UserName TEXT,'
                        'First_Name TEXT,'
                        'Last_Name TEXT,'
                        'Reg_Date TEXT)')
        connect.commit()
        cursor.close()
        connect.close()
    except Excetion as e:
        print(e)


def notInLists(message): # проверка есть ли пользователь в каком-либо списке
    try:
        return True
    except Exception as e:
        print(e)


@bot.message_handler(commands=['start'])
def handler_start(message):
    try:
        log(message)
        createTables()
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
        if notInLists(message):
            key1 = types.InlineKeyboardMarkup()
            key1.add(types.InlineKeyboardButton(text=helpButtonName, callback_data='0'))
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Welcome</b>')
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Узнать как пользоваться ботом</b>', reply_markup=key1)
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Вы что-то делаете...</b>')
    except Exception as e:
        print(e)


def timer():
    try:
        print('start')
        can=True
        while True:
            try:
                if int(datetime.now().strftime('%M'))%5==0 and int(datetime.now().strftime('%S'))==0:
                    if can:
                        bot.send_message(496537969, 'test')
                        bot.send_message(441287694, 'ti priemniy')
                        print('sending')
                    can=False
                else:
                    can=True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)


try: # максимально странная конструкция
    while True:
        t=threading.Thread(target=timer, name='timer')
        t.start()
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(e)
except Exception as e:
    print(e)

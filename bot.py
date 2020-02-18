"""
файл для обработки команд
"""
from datetime import datetime
from telebot import types
import threading
import functions
import loopWork
import dataBase
import sqlite3
import telebot
import random
import time
import args
import os

bot = telebot.TeleBot(args.token)
techList = ['программист', 'математик']
gumList = ['Миша', 'ленивая жопа']
nickList = []
print(bot.get_me())


@bot.message_handler(commands=['start'])
def handler_start(message):
    try:
        functions.log(message)
        dataBase.createTables()
        key1 = types.InlineKeyboardMarkup()
        key1.add(types.InlineKeyboardButton(text=args.helpButtonName, callback_data='0'))
        try:
            bot.send_sticker(message.from_user.id, args.hello)
        except Exception as e:
            print(e)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Узнать как пользоваться ботом</b>',
                         reply_markup=key1)
        contain = False
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
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
            data = [message.from_user.id, message.from_user.username, "None", "None", "None", str(args.waitStatus), 0, 0,
                    str(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        connect.commit()
    except Exception as e:
        print(e)


@bot.message_handler(commands=['log'])  # функция обработки запроса логов
def handler_log(message):
    try:
        functions.log(message)
        if functions.isAdmin(message.from_user.id):
            doc = open(args.filesFolderName + args.logFileName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['db'])  # функция обработки запроса базы данных
def handler_db(message):
    try:
        functions.log(message)
        if functions.isAdmin(message.from_user.id):
            doc = open(args.filesFolderName + args.databaseName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['add_quest'])  # функция обработки запроса логов
def handler_add_quest(message):
    try:
        functions.log(message)
        dataBase.add_Quest(message)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['help'])  # обработка команды помощи
def handler_help(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='Меню помощи\n'
                                                                               '/start - Начать ользоваться ботом\n'
                                                                               '/help - Меню помощи\n'
                                                                               '/accept - Согласиться на выполнение работы\n'
                                                                               '/cancel - Отказаться от выполнения работы\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-\n'
                                                                               '-')
        if functions.isAdmin(message.from_user.id):
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='Меню помощи\n'
                                                                                   '/log - Запросить логи\n'
                                                                                   '/db - Запросить базу данных\n'
                                                                                   '/add_quest - (по формату /add_quest , профессия , задание , ранг , время)\n'
                                                                                   '-\n'
                                                                                   '-\n'
                                                                                   '-\n'
                                                                                   '-\n'
                                                                                   '-\n'
                                                                                   '-')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['quest'])  # функция обработки запроса логов
def handler_quest(message):
    try:
        dataBase.UpdProf()
        dataBase.UpdQuests()
        functions.log(message)
        quests = args.QuestsArr
        res = " "
        for Qest in quests:
            for i in Qest:
                res += str(i) + " "
            res += "\n"
        bot.send_message(message.from_user.id, str(res))
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
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if message.text == args.acceptWorkButton or message.text == args.cancelWorkButton:
            if message.text == args.acceptWorkButton:
                dataBase.change_status(message.from_user.id, args.workStatus, datetime.now().strftime('%M'))
        elif message.text == args.helpButtonName:
            o = 0
        elif message.text in techList or message.text in gumList:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row(args.helpButtonName)
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
                             text='<i>Ваша профессия </i><b>' + message.text + '</b>', reply_markup=user_markup)
            connect.commit()
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<i>Теперь укажите ваш никнейм </i>', reply_markup=user_markup)
            nickList.append(message.from_user.id)
        elif message.from_user.id in nickList:
            index = nickList.index(message.from_user.id)
            dataBase.set_nickname(message)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Ваш никнейм ' + message.text + '</b>')
            nickList.pop(index)
        else:
            cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
            spec = cursor.fetchall()
            if spec[0][0] == 'None':
                print('ggg')
                if message.text == "6":
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>Поздравляем, вы-технарь</b>')
                    cursor.execute("UPDATE Users SET Spec='tech' WHERE ID=" + str(message.from_user.id))
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    user_markup.row(techList[0], techList[1])
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь вы можете выбрать одну из предложенных профессий</i>',
                                     reply_markup=user_markup)
                    try:
                        bot.send_sticker(message.from_user.id, args.choose)
                    except Exception as e:
                        print(e)
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
            else:
                bot.send_message(message.from_user.id, message.text)
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


try:  # максимально странная конструкция
    while True:
        t = threading.Thread(target=loopWork.timer, name='timer', args=[bot])  # создание потока для функции timer
        t.start()  # запуск потока
        try:
            bot.polling(none_stop=True, interval=0)  # получение обновлений
        except Exception as e:
            print(e)
except Exception as e:
    print(e)

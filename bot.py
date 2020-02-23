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
import args

print("------------------------НАЧАЛАСЬ ЗАГРУЗКА БОТА------------------------")
bot = telebot.TeleBot(args.token)
dataBase.createTables()
dataBase.UpdProf()
dataBase.UpdQuests()
args.bot = bot
print("------------------------ЗАКОНЧИЛАСЬ ЗАГРУЗКА БОТА------------------------")

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
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=args.test_question)
            data = [message.from_user.id, message.from_user.username, "None", "None", "None", str(args.waitStatus),
                    "None", 0, str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')), 0, "0"]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
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
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='Меню помощи\n'
                              '/start - Начать ользоваться ботом\n'
                              '/help - Меню помощи\n'
                              '/accept - Согласиться на выполнение работы\n'
                              '/cancel - Отказаться от выполнения работы\n'
                              '/give_task - Дать задание другому игроку\n'
                              '/change_spec - Изменить специализацию\n'
                              '-\n'
                              '-\n'
                              '-')
        if functions.isAdmin(message.from_user.id):
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='Меню помощи\n'
                                  '/log - Запросить логи\n'
                                  '/db - Запросить базу данных\n'
                                  '/add_quest - (по формату '
                                  '/add_quest , профессия , задание , ранг , время)\n '
                                  '-\n'
                                  '-\n'
                                  '-\n'
                                  '-\n'
                                  '-\n'
                                  '-')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['quest'])  # функция обработки всех квестов
def handler_quest(message):
    try:
        functions.log(message)
        dataBase.UpdProf()
        dataBase.UpdQuests()
        functions.log(message)
        quests = args.QuestsArr
        res = ""
        for Qest in quests:
            for i in Qest:
                res += str(i) + " "
            res += "\n"
        bot.send_message(message.from_user.id, str(res))
    except Exception as e:
        print(e)


@bot.message_handler(commands=['give_task'])  # функция выдачи задания
def handler_giveTask(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='<b>Выберете кому дать дать задание:\n</b>' + str(dataBase.get_workers(message)))
    except Exception as e:
        print(e)


@bot.message_handler(commands=['accept'])  # функция выдачи задания
def handler_accept(message):
    try:
        functions.log(message)
        if dataBase.isFree(message.from_user.id):
            job_timer = 1
            dataBase.start_job(message.from_user.id, args.workStatus,
                               (int(datetime.now().strftime('%M')) + job_timer) % 60)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<i>Вы Начали выполнение здания это займет примерно</i> <b>' + str(
                                 job_timer) + '</b> <i> мин</i>')
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>OOPS\nВы заняты чем-то другим</b>')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['cancel'])  # функция выдачи задания
def handler_cancel(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='<b>Вы отказались от выполнения задания</b>')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['change_spec'])  # функция выдачи задания
def handler_cancel(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=args.test_question)
        dataBase.change_spec(message.from_user.id)
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
        if len(message.text) > 5:
            if str(message.text[1] + message.text[2] + message.text[3] + message.text[4]) == 'task':
                workerID = int(message.text[5:])
                if workerID != message.from_user.id:
                    if dataBase.isFree(workerID):
                        functions.send_task(workerID, dataBase.get_nickname(message.from_user.id),
                                            dataBase.get_task(message.from_user.id))
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<i>Вы отправили задание пользователю</i> <b>' + str(
                                             dataBase.get_nickname(workerID)) + '</b>')
                    else:
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>OOPS\nКажется пользователь занят</b>')
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>А ты хитрый жук, не делай так больше</b>')
                return
        if message.text == args.acceptWorkButton or message.text == args.cancelWorkButton:
            if message.text == args.acceptWorkButton:
                handler_accept(message)
            elif message.text == args.cancelWorkButton:
                handler_cancel(message)
        elif message.text == args.helpButtonName or message.from_user.id in nickList:
            if message.text == args.helpButtonName:
                handler_help(message)
            else:
                index = nickList.index(message.from_user.id)
                dataBase.set_nickname(message)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Ваш никнейм</i> <b>' + message.text + '</b>')
                nickList.pop(index)
        elif message.text in args.techList or message.text in args.gumList or message.text in args.lowList:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row(args.helpButtonName)
            if dataBase.set_profession(message, False):
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Ваша профессия</i> <b>' + message.text + '</b>', reply_markup=user_markup)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Теперь укажите ваш никнейм </i>', reply_markup=user_markup)
                nickList.append(message.from_user.id)
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Произошла ошибка, повторите попытку позже</b>')
        elif message.from_user.id in args.new_frof_list:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row(args.helpButtonName)
            dataBase.set_profession(message, functions.in_profArr(message.text))
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<i>Ваша новая профессия</i> <b>' + message.text + '</b>', reply_markup=user_markup)
        else:
            if dataBase.get_spec(message.from_user.id) == 'None':
                if message.text == "6":
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Поздравляем, вы — </i><b>технарь</b>')
                    dataBase.upd_spec(message.from_user.id, 'tech')
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    for i in args.techList:
                        user_markup.row(i)
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь вы можете выбрать одну из предложенных профессий</i>',
                                     reply_markup=user_markup)
                    try:
                        bot.send_sticker(message.from_user.id, args.choose)
                    except Exception as e:
                        print(e)
                elif str(message.text).isnumeric():
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Соболезнуем, вы — </i><b>гуманитарий</b>')
                    dataBase.upd_spec(message.from_user.id, 'gum')
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    for i in args.gumList:
                        user_markup.row(i)
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь вы можете выбрать одну из предложенных профессий</i>',
                                     reply_markup=user_markup)
                    try:
                        bot.send_sticker(message.from_user.id, args.choose)
                    except Exception as e:
                        print(e)
                else:
                    print('check')
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>Походу у вас с головой проблемы</b>')
                    dataBase.upd_spec(message.from_user.id, "low")
                    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
                    for i in args.lowList:
                        user_markup.row(i)
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь вы можете выбрать одну из предложенных профессий</i>',
                                     reply_markup=user_markup)
                    try:
                        bot.send_sticker(message.from_user.id, args.choose)
                    except Exception as e:
                        print(e)
            else:
                bot.send_message(message.from_user.id, message.text)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['photo'])  # функция обработки фото
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['contact'])  # функция обработки фото
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['sticker'])  # функция обработки фото
def handler_photo(message):
    try:
        if not functions.isAdmin(message.from_user.id):
            functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
        else:
            file_info = bot.get_file(message.sticker.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            print(downloaded_file)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['voice'])  # функция обработки фото
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['location'])  # функция обработки фото
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['audio'])  # функция обработки фото
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['video'])  # функция обработки фото
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['document'])  # функция обработки фото
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        print(e)


try:  # максимально странная конструкция
    while True:
        t = threading.Thread(target=loopWork.timer, name='timer', args=[bot])  # создание потока для функции timer
        t.start()  # запуск потока
        try:
            bot.polling(none_stop=True, interval=0)  # получение обновлений
        except Exception as er:
            print(er)
except Exception as er:
    print(er)

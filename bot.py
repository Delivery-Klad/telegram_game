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
                    "None", 0, str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')), 0, "0", 0, "0", 0]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
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
                              '/corp_help - Информация об организациях\n'
                              '-\n'
                              '-')
        if functions.isAdmin(message.from_user.id):
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='Меню помощи\n'
                                  '/log - Запросить логи\n'
                                  '/db - Запросить базу данных\n'
                                  '/add_quest - (по формату '
                                  '/add_quest , профессия , задание , ранг , время)\n '
                                  '/upd_quests and /upd_profs обновляют массивы'
                                  '-\n'
                                  '-\n'
                                  '-\n'
                                  '-\n'
                                  '-')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['upd_quests'])  # функция обработки всех квестов
def handler_quest(message):
    try:
        functions.log(message)
        dataBase.UpdQuests()
        functions.log(message)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['upd_profs'])  # функция обработки всех квестов
def handler_quest(message):
    try:
        functions.log(message)
        dataBase.UpdProf()
        functions.log(message)
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
        if dataBase.can_accept(message.from_user.id):
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
        elif dataBase.can_accept_corp(message.from_user.id):
            dataBase.upd_corp(message.from_user.id, 'Какая-то компания')
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы приняли приглос в организацию</b>')
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>OOPS</b>\nКажется у вас нет задания, которое можно принять')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['cancel'])  # функция выдачи задания
def handler_cancel(message):
    try:
        functions.log(message)
        if dataBase.can_accept(message.from_user.id):
            dataBase.upd_can_accept(message.from_user.id, 0)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы отказались от выполнения задания</b>')
        elif dataBase.can_accept_corp(message.from_user.id):
            dataBase.upd_corp(message.from_user.id, 0)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы отказались от вступления в организацию</b>')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['change_spec'])  # функция выдачи задания
def handler_changeSpec(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=args.test_question)
        dataBase.change_spec(message.from_user.id)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['invite_to_corp'])  # функция инвайта в орг
def handler_invite(message):
    try:
        functions.log(message)
        if dataBase.isOwner(message.from_user.id):
            company = dataBase.get_company(message.from_user.id)
            userID = message.text.split(maxsplit=1)
            userID = userID[1]
            if not dataBase.inCorp(userID):
                '''bot.send_message(parse_mode='HTML', chat_id=int(userID), text='Пользователь {0} пригласил вас в '
                                                                              'организацию {1}'.format(str(dataBase.
                                                                                get_nickname(message.from_user.id)), company))'''
                bot.send_message(chat_id=int(userID), text='Вы были приглашены в организацию "{}"'.format(company))
                dataBase.newReq(userID, company)
                print(userID)
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Пользователь уже состоит в организации</b>')
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Кажется вы не глава организации</b>')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['kick'])  # функция инвайта в орг
def handler_kick(message):
    try:
        functions.log(message)
        if dataBase.isOwner(message.from_user.id):
            userID = int(message.text[5:])
            print(userID)
            try:
                if int(userID) != int(message.from_user.id):
                    if dataBase.inCorp(userID):
                        bot.send_message(parse_mode='HTML', chat_id=userID,
                                         text='<b>Вас выгнали из организации</b>')
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>Пользователь исключен из организации</b>')
                        dataBase.kick_from_corp(userID)
                    else:
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>Пользователь не состоит в организации</b>')
            except Exception as e:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<bВы не можете исключить сами себя из организации</b>')
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы не глава организации</b>')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['corp_members'])  # функция инвайта в орг
def handler_members(message):
    try:
        functions.log(message)
        members = dataBase.corp_members(message.from_user.id)
        msg = '<b>Члены организации:</b>\n' + members
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text=msg)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['leave_corp'])  # функция инвайта в орг
def handler_leave(message):
    try:
        functions.log(message)
        if dataBase.inCorp(message.from_user.id):
            company = dataBase.get_company(message.from_user.id)
            if dataBase.leave_corp(message.from_user.id):
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Вы покинули организацию</b> <i>{0}</i>'.format(str(company)))
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Владелец не может покинуть организацию</b>')
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы не состоите в организации</b>')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['corp_help'])  # функция инвайта в орг
def handler_corp_help(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='Меню помощи\n'
                              '/create_corp - Создать организацию\n'
                              '/leave_corp - Покинуть организацию\n'
                              '/accept - Согласиться вступить в организацию\n'
                              '/cancel - Отказаться от вступления в организацию\n'
                              '/kick + id - Выгнать из организации\n'
                              '/invite_to_corp + id - Приглос в организацию\n'
                              '/corp_members - Информация о членах организации\n'
                              '-\n'
                              '-')
    except Exception as e:
        print(e)


@bot.message_handler(commands=['create_corp'])  # функция инвайта в орг
def handler_create_corp(message):
    try:
        functions.log(message)
        if dataBase.get_rank(message.from_user.id) == args.maxrank:
            name = message.text.split(maxsplit=1)
            name = name[1]
            print(name)
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Организацию может создать только пользователь достигший дзена</b>')
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
                                            dataBase.get_task(workerID))
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<i>Вы отправили задание пользователю</i> <b>' + str(
                                             dataBase.get_nickname(workerID)) + '</b>')
                        dataBase.upd_can_accept(workerID, 1)
                    else:
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>OOPS\nКажется пользователь занят</b>')
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>А ты хитрый жук, не делай так больше</b>')
                return
            elif str(message.text[1] + message.text[2] + message.text[3] + message.text[4]) == 'kick':
                handler_kick(message)
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
                if dataBase.get_nickname(message.from_user.id) == "None":
                    print('2')
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

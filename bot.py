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
bot = telebot.TeleBot(token=args.token)
dataBase.create_tables()
dataBase.upd_prof()
dataBase.upd_quests()
args.bot = bot
nickList = []
avatarList = []
print(bot.get_me())
print("------------------------ЗАКОНЧИЛАСЬ ЗАГРУЗКА БОТА------------------------")


@bot.message_handler(commands=['start'])
def handler_start(message):
    try:
        functions.log(message)
        key1 = types.InlineKeyboardMarkup()
        key1.add(types.InlineKeyboardButton(text=args.helpButtonName, callback_data='0'))
        try:
            bot.send_sticker(message.from_user.id, args.hello)
        except Exception as e:
            functions.error_log(e)
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
            try:
                mess = message.text.split()
                res = mess[1]
            except Exception as e:
                functions.error_log(e)
                res = 0
            data = [message.from_user.id, message.from_user.username, "None", "None", "None", str(args.waitStatus),
                    "None", 0, str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')), 0, "0", 0, "0", 0,
                    "None", "None", res]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
        connect.commit()
    except Exception as e:
        functions.error_log(e)


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
                              '/me - Информация об аккаунте\n'
                              '/balance - Узнать баланс\n'
                              '/change_nickname - Изменить никнейм\n'
                              '-')
        if functions.isAdmin(message.from_user.id):
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='Меню помощи\n'
                                  '/log - Запросить логи\n'
                                  '/error_log() - Запросить логи\n'
                                  '/db - Запросить базу данных\n'
                                  '/add_quest - (по формату '
                                  '/add_quest , профессия , задание , ранг , время)\n '
                                  '-')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['corp_help'])  # функция инвайта в орг
def handler_corp_help(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='Меню помощи\n'
                              '/create_corp (+название) - Создать организацию\n'
                              '/leave_corp - Покинуть организацию\n'
                              '/set_desc (+название) - Добавить описание организации\n'
                              '/info - Информация об организации\n'
                              '/accept - Согласиться вступить в организацию\n'
                              '/cancel - Отказаться от вступления в организацию\n'
                              '/invite - Выбрать кому отправить приглос в орг\n'
                              '/corp_members - Информация о членах организации\n'
                              '/get_task - Получить задание на организацию\n'
                              '-')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['log'])  # функция обработки запроса логов
def handler_log(message):
    try:
        functions.log(message)
        if functions.isAdmin(message.from_user.id):
            doc = open(args.filesFolderName + args.logFileName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['db'])  # функция обработки запроса базы данных
def handler_db(message):
    try:
        functions.log(message)
        if functions.isAdmin(message.from_user.id):
            doc = open(args.filesFolderName + args.databaseName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['ref'])
def handler_ref(message):
    functions.log(message)
    bot.send_message(chat_id=message.from_user.id, text="Реферальная ссылка для помощи проекту и себе: "
                                                        "https://telegram.me/" + bot.get_me().username + "?start={}"
                     .format(message.from_user.id))


@bot.message_handler(commands=['balance'])
def handler_balance(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='<i>Ваш баланс: </i>' + str(dataBase.get_balance(message.from_user.id)))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['add_quest'])  # функция обработки запроса логов
def handler_add_quest(message):
    try:
        functions.log(message)
        dataBase.add_quest(message)
        dataBase.upd_quests()
        dataBase.upd_prof()
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['give_task'])  # функция выдачи задания
def handler_giveTask(message):
    try:
        functions.log(message)
        msg, markup = dataBase.get_workers(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='<b>Выберете кому дать дать задание:\n</b>' + msg, reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['invite'])  # функция инвайта в орг
def handler_org(message):
    try:
        if dataBase.is_owner(message.from_user.id):
            functions.log(message)
            msg, markup = dataBase.get_not_in_corp_users(message)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Выберете кому кинуть приглашение:\n</b>' + msg, reply_markup=markup)
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Вы не владелец компании</b>')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['accept'])
def handler_accept(message):
    try:
        functions.log(message)
        if dataBase.can_accept(message.from_user.id):
            if dataBase.is_free(message.from_user.id):
                job_timer = dataBase.get_job_timer(message.from_user.id)
                dataBase.start_job(message.from_user.id, args.workStatus,
                                   (int(datetime.now().strftime('%M')) + job_timer) % 60)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Вы Начали выполнение здания это займет примерно</i> <b>' + str(
                                     job_timer) + '</b> <i> мин</i>')
                return True
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>OOPS\nВы заняты чем-то другим</b>')
                return False
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>OOPS</b>\nКажется у вас нет задания, которое можно принять')
            return False
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['cancel'])
def handler_cancel(message):
    try:
        functions.log(message)
        if dataBase.can_accept(message.from_user.id):
            dataBase.upd_can_accept(message.from_user.id, 0)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы отказались от выполнения задания</b>')
            return True
        else:
            return False
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['change_spec'])
def handler_changeSpec(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=args.test_question)
        dataBase.change_spec(message.from_user.id)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['exit'])
def handler_exit(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>Выход только в окно</i>')
    except Exception as e:
        functions.error_log(e)


def handler_invite(message):
    try:
        functions.log(message)
        if dataBase.is_owner(message.from_user.id):
            company = dataBase.get_corp(message.from_user.id)
            try:
                userID = int(message.text[7:])
            except AttributeError:
                userID = int(message.data[7:])
            if dataBase.check_requests(userID, company):
                if not dataBase.in_corp(userID):
                    bot.send_message(parse_mode='HTML', chat_id=int(userID),
                                     text='Вы были приглашены в организацию "{}"'.format(company))
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='Вы пригласили <b>{}</b> в организацию '.format(
                                         dataBase.get_nickname(userID)))
                    dataBase.new_req(userID, company)
                    msg, markup = dataBase.get_request(userID)
                    bot.send_message(parse_mode='HTML', chat_id=int(userID),
                                     text='<b>Список ваших приглашений:\n</b>' + msg, reply_markup=markup)
                    return True
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>Пользователь уже состоит в организации</b>')
                    return False
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>У пользователя уже есть приглашение в данную организацию</b>')
                return False
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Кажется вы не глава организации</b>')
            return False
    except Exception as e:
        functions.error_log(e)


def handler_kick(message):
    try:
        functions.log(message)
        if dataBase.is_owner(message.from_user.id):
            try:
                userID = int(message.text[5:])
            except AttributeError:
                userID = int(message.data[5:])
            try:
                if int(userID) != int(message.from_user.id):
                    if dataBase.in_corp(userID):
                        bot.send_message(parse_mode='HTML', chat_id=userID,
                                         text='<b>Вас выгнали из организации</b>')
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>Пользователь исключен из организации</b>')
                        dataBase.kick_from_corp(userID)
                        return True
                    else:
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>Пользователь не состоит в организации</b>')
                        return False
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<bВы не можете исключить сами себя из организации</b>')
                    return False
            except Exception as e:
                functions.error_log(e)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<bВы не можете исключить сами себя из организации</b>')
                return False
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы не глава организации</b>')
            return False
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['corp_members'])  # члены компании
def handler_members(message):
    try:
        functions.log(message)
        msg, markup = dataBase.corp_members(message.from_user.id)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text=msg, reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['leave_corp'])  # функция ухода из орг
def handler_leave(message):
    try:
        functions.log(message)
        if dataBase.in_corp(message.from_user.id):
            company = dataBase.get_corp(message.from_user.id)
            if dataBase.leave_corp(message.from_user.id):
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Вы покинули организацию</b> <i>{0}</i>'.format(str(company)))
                return True
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Владелец не может покинуть организацию</b>')
                return False
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы не состоите в организации</b>')
            return False
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['get_task'])  # функция ухода из орг
def handler_get_task(message):
    try:
        functions.log(message)
        if dataBase.in_corp(message.from_user.id):
            if dataBase.is_owner(message.from_user.id):
                dataBase.refresh_corp_tasks(message.from_user.id)
                msg, markup = dataBase.get_corp_task(message.from_user.id)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=msg, reply_markup=markup)
                return True
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Вы не глава организации</b>')
                return False
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы не состоите в организации</b>')
            return False
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['create_corp'])  # функция инвайта в орг
def handler_create_corp(message):
    try:
        functions.log(message)
        if dataBase.get_user_rank(message.from_user.id) >= args.maxrank:
            if not dataBase.in_corp(message.from_user.id):
                if int(dataBase.get_balance(message.from_user.id)[:-1]) >= args.corp_cost:
                    try:
                        if len(message.text) == 12:
                            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                             text='<b>Вы не указали название организации</b>')
                        else:
                            name = message.text.split(maxsplit=1)
                            name = name[1]
                            dataBase.create_corp(message.from_user.id, name)
                            dataBase.set_owner(message.from_user.id)
                            dataBase.minus_money(message.from_user.id, args.corp_cost)
                            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                             text='<i>Организация</i> <b>' + name + '</b> <i>успешно создана</i>')
                    except Exception as e:
                        functions.error_log(e)
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Для создания организации требуется</i> <b>' + str(args.corp_cost) +
                                          str(args.currency) + '</b>')
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>OOPS\nВы уже состоите в организации</b>')
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Организацию может создать только пользователь достигший дзена</b>')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['info'])
def handler_info_corp(message):
    try:
        functions.log(message)
        info = dataBase.corp_info(message.from_user.id)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=info)
    except Exception as e:
        print(e)
        functions.error_log(e)


@bot.message_handler(commands=['set_desc'])
def handler_set_desc(message):
    try:
        functions.log(message)
        name = message.text.split(' ', 1)[1]
        res = dataBase.update_corp_description(message.from_user.id, name)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=res)
    except Exception as e:
        functions.error_log(e)


def handler_task(message):
    try:
        workerID = int(message.data[5:])
        if workerID != message.from_user.id:
            if dataBase.is_free(workerID):
                markup = types.InlineKeyboardMarkup()
                key1 = types.InlineKeyboardButton(args.acceptWorkButton, callback_data='1')
                key2 = types.InlineKeyboardButton(args.cancelWorkButton, callback_data='2')
                markup.add(key1)
                markup.add(key2)
                task_ = dataBase.get_task(workerID)
                dataBase.upd_task_now(workerID, task_)
                bot.send_message(parse_mode='HTML', chat_id=workerID,
                                 text=functions.send_task(dataBase.get_nickname(message.from_user.id),
                                                          task_), reply_markup=markup)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Вы отправили задание пользователю</i> <b>' + str(
                                     dataBase.get_nickname(workerID)) + '</b>')
                dataBase.upd_can_accept(workerID, 1)
                return True
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>OOPS\nКажется пользователь занят</b>')
                return False
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>А ты хитрый жук, не делай так больше</b>')
            return False
    except Exception as e:
        functions.error_log(e)


def handler_corp_task(message):
    try:
        if dataBase.is_owner(message.from_user.id):
            tmp = message.data.split('_')
            taskID = tmp[2]
            userID = tmp[1][4:]
            if dataBase.is_free(userID):
                markup = types.InlineKeyboardMarkup()
                key1 = types.InlineKeyboardButton(args.acceptWorkButton, callback_data='1')
                key2 = types.InlineKeyboardButton(args.cancelWorkButton, callback_data='2')
                markup.add(key1)
                markup.add(key2)
                msg = dataBase.give_corp_task(taskID, userID)
                if msg != 'None':
                    dataBase.upd_can_accept(userID, 1)
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Задание отправлено</i>')
                    bot.send_message(parse_mode='HTML', chat_id=int(userID),
                                     text=msg, reply_markup=markup)
                    return True
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Задание не отправлено</i>')
                    return False
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Пользователь занят</i>')
            return False
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Кажется вы не глава организации</b>')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['me'])  # функция инвайта в орг
def handler_me(message):
    try:
        functions.log(message)
        ids = message.from_user.id
        markup = types.InlineKeyboardMarkup()
        if dataBase.is_owner(ids):
            who = 'Ген.дир.'
        else:
            who = 'Работник'
        company = dataBase.get_corp_name(dataBase.get_corp(ids))
        if company == '0':
            company = 'Отсутствует'
            markup = None
        else:
            key = types.InlineKeyboardButton('Покинуть организацию', callback_data='/leave_corp')
            markup.add(key)
        msg = '<i>Никнейм: </i> <b>{5}</b>\n<i>Профессия:</i> <b>{0}</b>\n<i>Ранг:</i> <b>{1}</b>\n<i>Баланс:</i> ' \
              '<b>{2}</b>\n<i>Организация:</i> <b>{3}</b>\n<i>Должность в орг.:</i> <b>{4}</b>'.\
            format(dataBase.get_prof(ids), dataBase.get_user_rank(ids), dataBase.get_balance(ids), company,
                   who, dataBase.get_nickname(ids))
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text=msg, reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['change_nickname'])  # функция инвайта в орг
def handler_change(message):
    try:
        functions.log(message)
        nickList.append(message.from_user.id)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Ввведите новый ник:</b>')
    except Exception as e:
        functions.error_log(e)


@bot.callback_query_handler(func=lambda c: True)  # функция обработки inline кнопок
def func(c):
    try:
        if c.data == '0':
            handler_help(c)
            bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text='<b>Узнать как пользоваться ботом</b>', reply_markup=None)
            bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Ты приемный')
        elif c.data == '1':
            if handler_accept(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Вы начали выполнение задания')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
        elif c.data == '2':
            if handler_cancel(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Вы отказались выполнять '
                                                                                        'задание')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
        elif c.data[1:7] == 'invite':
            if handler_invite(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Пользователь приглашен')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Приглашение не отправлено')
        elif c.data[1:5] == 'task':
            if handler_task(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Задание отправлено')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Задание не отправлено')
        elif c.data[1:7] == 'accept':
            """
            
            пофиксить
            
            """
            owner_id = int(c.data[7:])
            company = dataBase.get_corp(owner_id)
            dataBase.upd_corp(c.from_user.id, company)
            dataBase.delete_request(c.from_user.id)
            bot.send_message(parse_mode='HTML', chat_id=owner_id, text='<b>{0} присоединился к организации</b>'.
                             format(str(dataBase.get_nickname(c.from_user.id))))
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                             text='<b>Вы присоединились к организации </b>' + str(company))
            bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Вы приняли приглашение')
        elif c.data[1:5] == 'kick':
            if handler_kick(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Пользователь исключен')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
        elif c.data[2:6] == 'task':
            if handler_corp_task(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Задание отправлено')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
        elif c.data[1:9] == 'give_low':
            if dataBase.is_owner(c.from_user.id):
                ids = str(c.data[9:])
                msg, markup = dataBase.get_low(c.from_user.id, ids)
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text=msg, reply_markup=markup)
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Success')
                return
            else:
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                 text='<b>Кажется вы не глава организации</b>')
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Error')
        elif c.data[1:9] == 'give_gum':
            if dataBase.is_owner(c.from_user.id):
                ids = str(c.data[9:])
                msg, markup = dataBase.get_gum(c.from_user.id, ids)
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text=msg, reply_markup=markup)
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Success')
                return
            else:
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                 text='<b>Кажется вы не глава организации</b>')
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Error')
        elif c.data[1:10] == 'give_tech':
            if dataBase.is_owner(c.from_user.id):
                ids = str(c.data[10:])
                msg, markup = dataBase.get_tech(c.from_user.id, ids)
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text=msg, reply_markup=markup)
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Success')
                return
            else:
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                 text='<b>Кажется вы не глава организации</b>')
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Error')
        elif c.data[1:] == 'leave_corp':
            if handler_leave(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Вы покинули орг')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['text'])  # функция обработки текстовых сообщений
def handler_text(message):
    try:
        functions.log(message)
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
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь укажите ваш никнейм </i>', reply_markup=user_markup)
                    nickList.append(message.from_user.id)
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Произошла ошибка, повторите попытку позже</b>')
        elif message.from_user.id in args.new_frof_list:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row(args.helpButtonName)
            dataBase.set_profession(message, functions.in_prof_arr(message.text))
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
                        functions.error_log(e)
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
                        functions.error_log(e)
                else:
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
                        functions.error_log(e)
            else:
                bot.send_message(message.from_user.id, message.text)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['photo'])
def handler_photo(message):
    try:
        ids = message.from_user.id
        if ids in avatarList:
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            dataBase.add_avatar(ids, downloaded_file)
            index = avatarList.index(ids)
            avatarList.pop(index)
            photo = dataBase.get_avatar(ids)
            bot.send_photo(chat_id=ids, photo=photo, caption='Ваш аватар')
        else:
            functions.wrong_input(ids, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['contact'])
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['sticker'])
def handler_photo(message):
    try:
        if not functions.isAdmin(message.from_user.id):
            functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
        else:
            file_info = bot.get_file(message.sticker.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['voice'])
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['location'])
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['audio'])
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['video'])
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['document'])
def handler_photo(message):
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


try:  # максимально странная конструкция
    while True:
        t = threading.Thread(target=loopWork.timer, name='timer')  # создание потока для функции timer
        t.start()  # запуск потока
        try:
            bot.polling(none_stop=True, interval=0)  # получение обновлений
        except Exception as er:
            functions.error_log(er)
        threading.active_count()
except Exception as er:
    functions.error_log(er)

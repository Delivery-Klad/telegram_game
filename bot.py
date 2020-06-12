"""
файл для обработки команд пользователя
"""
import os
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
            data = [message.from_user.id, "None", "None", "None", str(args.waitStatus),
                    "None", 0, 0, "0", 0, 0, 0, "None"]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
            data = [message.from_user.id, message.from_user.username,
                    str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')), res]
            cursor.execute('INSERT INTO HiddenInfo VALUES(?, ?, ?, ?)', data)
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
                              '/ref - Реферальная ссылка\n'
                              '/top - Посмотреть топ\n'
                              '/give_task - Дать задание другому игроку\n'
                              '/change_spec - Изменить специализацию (ранг будет сброшен)\n'
                              '/change_prof - Изменить профессию (в разработке)\n'
                              '/corp_help - Информация об организациях\n'
                              '/me - Информация об аккаунте\n'
                              '/balance - Узнать баланс\n'
                              '/change_nickname - Изменить никнейм')
        if functions.is_admin(message.from_user.id):
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='Меню помощи\n'
                                  '/a (+сообщение) - Админ чат\n'
                                  '/log - Запросить логи\n'
                                  '/errors - Запросить ошибки\n'
                                  '/db - Запросить базу данных\n'
                                  '/add_quest - (по формату /add_quest , профессия , задание , ранг , время)')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['corp_help'])  # функция инвайта в орг
def handler_corp_help(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='Меню помощи организации\n'
                              '/info - Информация об организации\n'
                              '/create_corp (+название) - Создать организацию\n'
                              '/remove_corp - Расформировать организацию\n'
                              '/leave_corp - Покинуть организацию\n'
                              '/set_desc (+название) - Изменить описание организации\n'
                              '/set_name (+название) - Изменить название организации\n'
                              '/invite - Выбрать кому отправить приглос в орг\n'
                              '/corp_members - Информация о членах организации\n'
                              '/get_task - Получить задание на организацию')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['log'])  # функция обработки запроса логов
def handler_log(message):
    try:
        functions.log(message)
        if functions.is_admin(message.from_user.id):
            doc = open(args.filesFolderName + args.logFileName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['errors'])  # функция обработки запроса ошибок
def handler_error(message):
    try:
        functions.log(message)
        if functions.is_admin(message.from_user.id):
            doc = open(args.filesFolderName + args.ErlogFileName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['db'])  # функция обработки запроса базы данных
def handler_db(message):
    try:
        functions.log(message)
        if functions.is_admin(message.from_user.id):
            doc = open(args.filesFolderName + args.databaseName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['ref'])
def handler_ref(message):
    try:
        functions.log(message)
        bot.send_message(chat_id=message.from_user.id, text="Реферальная ссылка для помощи проекту и себе: "
                                                            "https://telegram.me/" + bot.get_me().username + "?start={}"
                         .format(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


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
def handler_give_task(message):
    try:
        functions.log(message)
        msg, markup = dataBase.get_workers(message.from_user.id)
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
def handler_change_spec(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=args.test_question)
        dataBase.change_spec(message.from_user.id)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['change_prof'])
def handler_change_prof(message):
    try:
        functions.log(message)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Фунция в разработке</b>')
        dataBase.give_new_prof(message.from_user.id)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['exit'])
def handler_exit(message):
    try:
        if functions.is_admin(message.from_user.id):
            functions.log(message)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>Выход только в окно</i>')
            os.abort()
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>Выход только в окно</i>')
    except Exception as e:
        functions.error_log(e)


def handler_invite(message):
    try:
        functions.log(message)
        if dataBase.is_owner(message.from_user.id):
            company = dataBase.get_corp(message.from_user.id)
            try:
                user_id = int(message.text[7:])
            except AttributeError:
                user_id = int(message.data[7:])
            if dataBase.check_requests(user_id, company):
                if not dataBase.in_corp(user_id):
                    bot.send_message(parse_mode='HTML', chat_id=int(user_id),
                                     text='Вы были приглашены в организацию "{}"'.format(company))
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='Вы пригласили <b>{}</b> в организацию '.format(
                                         dataBase.get_nickname(user_id)))
                    dataBase.new_req(user_id, company)
                    msg, markup = dataBase.get_request(user_id)
                    bot.send_message(parse_mode='HTML', chat_id=int(user_id),
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
                user_id = int(message.text[5:])
            except AttributeError:
                user_id = int(message.data[5:])
            try:
                if int(user_id) != int(message.from_user.id):
                    if dataBase.in_corp(user_id):
                        bot.send_message(parse_mode='HTML', chat_id=user_id,
                                         text='<b>Вас выгнали из организации</b>')
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>Пользователь исключен из организации</b>')
                        dataBase.kick_from_corp(user_id)
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


def handler_set_owner(message):
    try:
        functions.log(message)
        if dataBase.is_owner(message.from_user.id):
            try:
                user_id = int(message.text[10:])
            except AttributeError:
                user_id = int(message.data[10:])
            try:
                if int(user_id) != int(message.from_user.id):
                    if dataBase.in_corp(user_id):
                        bot.send_message(parse_mode='HTML', chat_id=user_id,
                                         text='<b>Вас назначили владельцем организации </b>' +
                                              dataBase.get_corp_name(dataBase.get_corp(user_id)))
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>Владелец успешно переназначен</b>')
                        dataBase.set_owner(message.from_user.id, 0)
                        dataBase.set_owner(user_id, 1)
                        return True
                    else:
                        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                         text='<b>Пользователь не состоит в организации</b>')
                        return False
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<bВы не можете назначить сами себя владельцем</b>')
                    return False
            except Exception as e:
                functions.error_log(e)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<bВы не можете назначить сами себя владельцем</b>')
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
            owner = int(dataBase.get_owner(dataBase.get_corp(message.from_user.id)))
            company = dataBase.get_corp_name(dataBase.get_corp(message.from_user.id))
            if dataBase.leave_corp(message.from_user.id):
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Вы покинули организацию</b> <i>{0}</i>'.format(str(company)))
                bot.send_message(parse_mode='HTML', chat_id=owner,
                                 text='<b>Пользователь {0} покинул организацию</b> <i>{1}</i>'.
                                 format(dataBase.get_nickname(message.from_user.id), company))
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
                            dataBase.set_owner(message.from_user.id, 1)
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


@bot.message_handler(commands=['remove_corp'])
def handler_del_corp(message):
    try:
        markup = types.InlineKeyboardMarkup()
        company = dataBase.get_corp(message.from_user.id)
        if company == '0':
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы не состоите в организации</b>')
            return
        if dataBase.is_owner(message.from_user.id):
            key1 = types.InlineKeyboardButton('Да', callback_data='/remove_accept')
            key2 = types.InlineKeyboardButton('Нет', callback_data='/remove_decline')
            markup.add(key1, key2)
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<b>Вы не владелец организации</b>')
            return
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Удалить организацию?</b>',
                         reply_markup=markup)
    except Exception as e:
        print(e)
        functions.error_log(e)


@bot.message_handler(commands=['info'])
def handler_info_corp(message):
    try:
        functions.log(message)
        info = dataBase.corp_info(message.from_user.id)
        markup = types.InlineKeyboardMarkup()
        company = dataBase.get_corp_name(dataBase.get_corp(message.from_user.id))
        if company == '0':
            markup = None
        else:
            key = types.InlineKeyboardButton('Покинуть организацию', callback_data='/leave_corp')
            markup.add(key)
        if dataBase.is_owner(message.from_user.id):
            key = types.InlineKeyboardButton('Передать командование', callback_data='/change_owner')
            markup.add(key)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=info, reply_markup=markup)
    except Exception as e:
        print(e)
        functions.error_log(e)


@bot.message_handler(commands=['set_desc'])
def handler_set_desc(message):
    try:
        functions.log(message)
        desc = message.text.split(' ', 1)[1]
        res = dataBase.update_corp_description(message.from_user.id, desc)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=res)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['set_name'])
def handler_set_name(message):
    try:
        functions.log(message)
        name = message.text.split(' ', 1)[1]
        res = dataBase.update_corp_name(message.from_user.id, name)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=res)
    except Exception as e:
        functions.error_log(e)


def handler_task(message):
    try:
        worker_id = int(message.data[5:])
        if worker_id != message.from_user.id:
            if dataBase.is_free(worker_id):
                markup = types.InlineKeyboardMarkup()
                key1 = types.InlineKeyboardButton(args.acceptWorkButton, callback_data='1')
                key2 = types.InlineKeyboardButton(args.cancelWorkButton, callback_data='2')
                markup.add(key1)
                markup.add(key2)
                task_ = dataBase.get_task(worker_id)
                dataBase.upd_task_now(worker_id, task_)
                bot.send_message(parse_mode='HTML', chat_id=worker_id,
                                 text=functions.send_task(dataBase.get_nickname(message.from_user.id),
                                                          task_), reply_markup=markup)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Вы отправили задание пользователю</i> <b>' + str(
                                     dataBase.get_nickname(worker_id)) + '</b>')
                dataBase.upd_can_accept(worker_id, 1)
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
            task_id = tmp[2]
            user_id = tmp[1][4:]
            if dataBase.is_free(user_id):
                markup = types.InlineKeyboardMarkup()
                key1 = types.InlineKeyboardButton(args.acceptWorkButton, callback_data='1')
                key2 = types.InlineKeyboardButton(args.cancelWorkButton, callback_data='2')
                markup.add(key1)
                markup.add(key2)
                msg = dataBase.give_corp_task(task_id, user_id)
                if msg != 'None':
                    dataBase.upd_can_accept(user_id, 1)
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Задание отправлено</i>')
                    bot.send_message(parse_mode='HTML', chat_id=int(user_id),
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


@bot.message_handler(commands=['me'])  # функция информации об аккаунте
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
        if dataBase.is_owner(message.from_user.id):
            key = types.InlineKeyboardButton('Передать командование', callback_data='/change_owner')
            markup.add(key)
        msg = '<i>Никнейм: </i> <b>{5}</b>\n<i>Профессия:</i> <b>{0}</b>\n<i>Ранг:</i> <b>{1}</b>\n<i>Баланс:</i> ' \
              '<b>{2}</b>\n<i>Организация:</i> <b>{3}</b>\n<i>Должность в орг.:</i> <b>{4}</b>'.\
            format(dataBase.get_prof(ids), dataBase.get_user_rank(ids), dataBase.get_balance(ids), company,
                   who, dataBase.get_nickname(ids))
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text=msg, reply_markup=markup)
    except Exception as e:
        print(e)
        functions.error_log(e)


@bot.message_handler(commands=['change_nickname'])  # функция изменения ника
def handler_change(message):
    try:
        functions.log(message)
        nickList.append(message.from_user.id)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Ввведите новый ник:</b>')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['top'])  # функция для посмотра топов
def handler_tops(message):
    try:
        functions.log(message)
        markup = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton('Топ богачей', callback_data='/top_rich')
        key2 = types.InlineKeyboardButton('Топ организаций', callback_data='/top_orgs')
        markup.add(key1)
        markup.add(key2)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Выберите из списка:\n</b>',
                         reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['a'])  # функция отправки сообщения в админ чат
def handler_a_chat(message):
    try:
        if functions.is_admin(message.from_user.id):
            functions.log(message)
            command = message.text.split(maxsplit=1)[1]
            for j in range(len(args.admins_list)):
                if args.admins_list[j] != message.from_user.id:
                    bot.send_message(parse_mode='HTML', chat_id=args.admins_list[j], text=str('Админ чат | {0} {1}').
                                     format(dataBase.get_nickname(message.from_user.id), command))
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
                bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id,
                                      text=c.message.text)
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
        elif c.data[1:10] == 'set_owner':
            if handler_set_owner(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Владелец обновлен')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
            bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text=c.message.text)
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
        elif c.data[1:] == 'change_owner':
            msg, markup = dataBase.change_owner(c.from_user.id)
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                             text=msg, reply_markup=markup)
        elif c.data[1:] == 'remove_accept':
            members = dataBase.remove_corp(c.from_user.id)
            for i in members:
                bot.send_message(parse_mode='HTML', chat_id=i, text='<b>Организация расформирована</b>')
                dataBase.upd_corp(i, 0)
            bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text='Организация удалена')
        elif c.data[1:] == 'remove_decline':
            bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text='Действие отменено')
        elif c.data[1:] == 'top_rich':
            res = dataBase.get_top('rich')
            bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id, text=res)
        elif c.data[1:] == 'top_orgs':
            res = dataBase.get_top('orgs')
            bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id, text=res)
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
        elif message.from_user.id in args.new_prof_list:
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
        if not functions.is_admin(message.from_user.id):
            functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
        else:
            file_info = bot.get_file(message.sticker.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            print(downloaded_file)
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


try:  # максимально странная конструкция (за то работает)
    while True:
        t = threading.Thread(target=loopWork.timer, name='timer')  # создание потока для функции timer
        t.start()  # запуск нового потока
        try:
            bot.polling(none_stop=True, interval=0)  # получение обновлений
        except Exception as er:
            functions.error_log(er)
        threading.active_count()
except Exception as er:
    functions.error_log(er)

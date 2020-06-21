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
import pg_connect
import telebot
import args

print("------------------------НАЧАЛАСЬ ЗАГРУЗКА БОТА------------------------")
bot = telebot.TeleBot(token=args.token)
dataBase.create_tables()
dataBase.upd_prof()
dataBase.upd_quests()
args.bot = bot
nickList = []
createCorpList = []
descriptionList = []
nameOfCorpList = []
avatarList = []
print(bot.get_me())
args.start_time = datetime.now()
print("------------------------ЗАКОНЧИЛАСЬ ЗАГРУЗКА БОТА------------------------")


@bot.message_handler(commands=['start'])
def handler_start(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
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
        connect, cursor = pg_connect.connect()
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
                    "None", 0, 0, "0", 0, 0, 0, 0, "None"]
            cursor.execute('INSERT INTO Users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', data)
            data = [message.from_user.id, message.from_user.username,
                    str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')), res, 0]
            cursor.execute('INSERT INTO HiddenInfo VALUES(?, ?, ?, ?, ?)', data)
        connect.commit()
        cursor.close()
        connect.close()
    except Exception as e:
        functions.error_log(e)


def handler_help(message):  # обработка команды помощи
    """
    :param message: сообщение от пользователя
    :return: меню помощи
    """
    try:
        functions.log(message)
        markup = inline_keyboard(message.from_user.id, False, False, False, True, False)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='Основное меню:', reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


def corp_help(user_id):  # функция помощи орг
    """
    :param user_id: user_id
    :return: меню помощи по организации
    """
    try:
        markup = inline_keyboard(user_id, False, False, False, False, True)
        bot.send_message(parse_mode='HTML', chat_id=user_id,
                         text='<b>Меню настроек организации:</b>', reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


def inline_keyboard(user_id, corp_menu: bool, me_menu: bool, admin: bool, main_menu: bool, corp_set: bool):
    """
    :param user_id: user_id
    :param corp_menu: True/False
    :param me_menu: True/False
    :param admin: True/False
    :param main_menu: True/False
    :param corp_set: True/False
    :return: пользовательская клавиатура
    """
    try:
        markup = types.InlineKeyboardMarkup()
        if main_menu:
            key1 = types.InlineKeyboardButton('📝Выдать задание', callback_data='/give_tsk')
            key2 = types.InlineKeyboardButton('🙇‍♂️Создать аватар', callback_data='/crt_avatar')
            markup.add(key1)
            markup.add(key2)
        elif corp_menu:
            if dataBase.is_owner(user_id):
                key1 = types.InlineKeyboardButton('❌Расформировать', callback_data='/remove_corp')
                key2 = types.InlineKeyboardButton('🔁Передать командование', callback_data='/change_owner')
                key3 = types.InlineKeyboardButton('📩Пригласить', callback_data='/toorginvite')
                key4 = types.InlineKeyboardButton('🙎🏿‍♂️Состав', callback_data='/corp_members')
                key5 = types.InlineKeyboardButton('📝Получить задания', callback_data='/get_task')
                key6 = types.InlineKeyboardButton('⚙️Настройки организации', callback_data='/corp_settings')
                markup.add(key1)
                markup.add(key2)
                markup.add(key3)
                markup.add(key4)
                markup.add(key5)
                markup.add(key6)
            else:
                key1 = types.InlineKeyboardButton('❌Покинуть', callback_data='/leave_corp')
                markup.add(key1)
        elif me_menu:
            key1 = types.InlineKeyboardButton('🔗Реферальная ссылка', callback_data='/ref')
            key2 = types.InlineKeyboardButton('✏Изменить никнейм', callback_data='/change_nickname')
            key3 = types.InlineKeyboardButton('✏Изменить специальность', callback_data='/change_spec')
            key4 = types.InlineKeyboardButton('✏Изменить профессию', callback_data='/change_prof')
            markup.add(key1)
            markup.add(key2)
            markup.add(key3)
            markup.add(key4)
        elif corp_set:
            if dataBase.in_corp(user_id):
                key1 = types.InlineKeyboardButton('✏Изменить описание', callback_data='/change_descr')
                key2 = types.InlineKeyboardButton('✏Изменить название', callback_data='/change_nameCorp')
                markup.add(key1)
                markup.add(key2)
            else:
                key3 = types.InlineKeyboardButton('📌Создать организацию', callback_data='/crt_org')
                markup.add(key3)
        elif admin:
            key1 = types.InlineKeyboardButton('Логи', callback_data='/log')
            key2 = types.InlineKeyboardButton('Ошибки', callback_data='/errors')
            key3 = types.InlineKeyboardButton('Время работы', callback_data='/uptime')
            key4 = types.InlineKeyboardButton('База даных', callback_data='/db')
            key5 = types.InlineKeyboardButton('Выключить телеграм бота', callback_data='/exit')
            markup.add(key1, key2)
            markup.add(key3, key4)
            markup.add(key5)
        else:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row(args.AboutMeButtonName, args.TopsButtonName)
            user_markup.row(args.helpButtonName, args.CorpMenuButtonName)
            if functions.is_admin(user_id):
                user_markup.row(args.AhelpButtonName)
            return user_markup
        return markup
    except Exception as e:
        print(e)


def handler_corp_menu(message):  # меню организации
    """
    :param message: сообщение от пользователя
    :return: меню организации
    """
    try:
        msg = dataBase.corp_info(message.from_user.id)
        if msg == 'Вы не состоите в организации':
            markup = None
        else:
            markup = inline_keyboard(message.from_user.id, True, False, False, False, False)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text=msg, reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


def handler_log(message):  # функция обработки запроса логов
    """
    :param message: сообщение от пользователя
    :return: файл логов бота
    """
    try:
        if functions.is_admin(message.from_user.id):
            doc = open(args.filesFolderName + args.logFileName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


def handler_error(message):  # функция обработки запроса ошибок
    """
    :param message: сообщение от пользователя
    :return: файл ошибок бота
    """
    try:
        if functions.is_admin(message.from_user.id):
            doc = open(args.filesFolderName + args.ErlogFileName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


def handler_db(message):  # функция обработки запроса базы данных
    """
    :param message: сообщение от пользователя
    :return: файл базы данных бота
    """
    try:
        functions.log(message)
        if functions.is_admin(message.from_user.id):
            doc = open(args.filesFolderName + args.databaseName, 'rb')
            bot.send_document(message.from_user.id, doc)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['change_db'])  # заменить бд
def handler_change_db(message):
    """
    :param message: сообщение от пользователя
    :return: замента файла базы данных
    """
    try:
        functions.log(message)
        args.change_db.append(message.from_user.id)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Отправьте файл базы данных</b>')
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['add_quest'])  # функция обработки запроса логов
def handler_add_quest(message):
    """
    :param message: сообщение от пользователя
    :return: добавление квеста в базу данных
    """
    try:
        functions.log(message)
        data = message.text.split(' , ')
        data.pop(0)
        dataBase.add_quest(data)
        dataBase.upd_quests()
        dataBase.upd_prof()
    except Exception as e:
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>ОШИБКА: Возможно указаны не все '
                                                                               'требуемые параметры</b>')
        functions.error_log(e)


def handler_give_task(message):  # функция выдачи задания
    """
    :param message: сообщение от пользователя
    :return: список свободных пользователей
    """
    try:
        functions.log(message)
        msg, markup = dataBase.get_workers(message.from_user.id)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                         text='<b>Выберете кому дать дать задание:\n</b>' + msg, reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


def handler_accept(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        functions.log(message)
        if dataBase.can_accept(message.from_user.id):
            if dataBase.is_free(message.from_user.id):
                if dataBase.is_corp_task(message.from_user.id):
                    dataBase.upd_is_corp_task(message.from_user.id, 0)
                    dataBase.upd_corp_count_works(dataBase.get_corp(message.from_user.id))
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


def handler_cancel(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
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


def handler_exit(message):
    """
    :param message: сообщение от пользователя
    :return: завершение работы бота
    """
    try:
        if functions.is_admin(message.from_user.id):
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>Выход только в окно</i>')
            os.abort()
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>Выход только в окно</i>')
    except Exception as e:
        functions.error_log(e)


def handler_invite(message):
    """
    :param message: сообщение от пользователя
    :return: список пользователей не состоящих в орг
    """
    try:
        functions.log(message)
        if dataBase.is_owner(message.from_user.id):
            company = dataBase.get_corp(message.from_user.id)
            corp_name = dataBase.get_corp_name(dataBase.get_corp(message.from_user.id))
            try:
                user_id = int(message.text[7:])
            except AttributeError:
                user_id = int(message.data[7:])
            if dataBase.check_requests(user_id, company):
                if not dataBase.in_corp(user_id):
                    bot.send_message(parse_mode='HTML', chat_id=int(user_id),
                                     text='Вы были приглашены в организацию "{}"'.format(corp_name))
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
    """
    :param message: сообщение от пользователя
    :return: None
    """
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
    """
    :param message: сообщение от пользователя
    :return: изменение владельца орг
    """
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


def handler_leave(message):  # функция ухода из орг
    """
    :param message: сообщение от пользователя
    :return: None
    """
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


def handler_create_corp(message):  # функция создания орг
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        functions.log(message)
        if dataBase.get_user_rank(message.from_user.id) >= args.maxrank:
            if not dataBase.in_corp(message.from_user.id):
                if int(dataBase.get_balance(message.from_user.id)[:-1]) >= args.corp_cost:
                    try:
                        name = message.text
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


def handler_set_desc(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        functions.log(message)
        res = dataBase.update_corp_description(message.from_user.id, message.text)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=res)
    except Exception as e:
        functions.error_log(e)


def handler_set_name(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        functions.log(message)
        res = dataBase.update_corp_name(message.from_user.id, message.text)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=res)
    except Exception as e:
        functions.error_log(e)


def handler_task(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        worker_id = int(message.data[5:])
        if worker_id != message.from_user.id:
            if dataBase.is_free(worker_id):
                if worker_id != dataBase.get_last_worker(message.from_user.id):
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
                    dataBase.set_last_worker(message.from_user.id, worker_id)
                    return True
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>OOPS\nВы не можете отправлять задания одному и тому же пользователю '
                                          'несколько раз подряд</b>')
                    return False
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
    """
    :param message: сообщение от пользователя
    :return: None
    """
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
                    dataBase.upd_is_corp_task(user_id, 1)
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


def handler_me(message):  # функция информации об аккаунте
    """
    :param message: сообщение от пользователя
    :return: инфорамция об аккаунте
    """
    try:
        ids = message.from_user.id
        if dataBase.is_owner(ids):
            who = 'Ген.дир.'
        else:
            who = 'Работник'
        company = dataBase.get_corp_name(dataBase.get_corp(ids))
        if company == '0':
            company = 'Отсутствует'
        markup = inline_keyboard(message.from_user.id, False, True, False, False, False)
        check = dataBase.check_avatar(message.from_user.id)
        if check:
            params = dataBase.get_avatar_params(message.from_user.id)
            functions.generate_avatar(params[0], params[1], params[2])
            photo = open(args.tempImageName, 'rb')
        else:
            photo = open(args.avatar_directory + args.standard_avatar_file_name[0], 'rb')
        msg = '<i>Никнейм: </i> <b>{5}</b>\n<i>Профессия:</i> <b>{0}</b>\n<i>Ранг:</i> <b>{1}</b>\n<i>Баланс:</i> ' \
              '<b>{2}</b>\n<i>Организация:</i> <b>{3}</b>\n<i>Должность в орг.:</i> <b>{4}</b>'. \
            format(dataBase.get_prof(ids), dataBase.get_user_rank(ids), dataBase.get_balance(ids), company,
                   who, dataBase.get_nickname(ids))
        bot.send_photo(parse_mode='HTML', chat_id=message.from_user.id,
                       photo=photo, caption=msg, reply_markup=markup)
        photo.close()
        if check:
            os.remove(args.tempImageName)
    except Exception as e:
        print(e)
        functions.error_log(e)


def handler_tops(message):  # функция для посмотра топов
    """
    :param message: сообщение от пользователя
    :return: меню выбора топа
    """
    try:
        functions.log(message)
        markup = types.InlineKeyboardMarkup()
        key1 = types.InlineKeyboardButton('💰Топ богачей', callback_data='/top_rich')
        key2 = types.InlineKeyboardButton('📈Топ организаций', callback_data='/top_orgs')
        markup.add(key1)
        markup.add(key2)
        bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Выберите из списка:\n</b>',
                         reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(commands=['a'])  # функция отправки сообщения в админ чат
def handler_a_chat(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
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


@bot.message_handler(commands=['all'])  # функция отправки сообщения в общий чат
def handler_a_chat(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        if functions.is_admin(message.from_user.id):
            functions.log(message)
            msg = message.text.split(maxsplit=1)[1]
            users = dataBase.get_all_users()
            markup = inline_keyboard(message.from_user.id, False, False, False, False, False)
            for i in range(len(users)):
                bot.send_message(parse_mode='HTML', chat_id=users[i], text=str('Сообщение от админа | {0} {1}').
                                 format(dataBase.get_nickname(message.from_user.id), msg), reply_markup=markup)
    except Exception as e:
        functions.error_log(e)


def handler_uptime(message):  # узнать время работы
    """
    :param message: сообщение от пользователя
    :return: время работы бота
    """
    try:
        if functions.is_admin(message.from_user.id):
            tmp_msg = str('<b>\nВремя:</b> ' + str(datetime.now() - args.start_time))
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text=str(tmp_msg))
    except Exception as e:
        functions.error_log(e)


def set_avatar(message):  # функция создания аватара
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        msg = message.text.split(' ')
        if not msg[0].isnumeric() or not msg[1].isnumeric() or not msg[2].isnumeric():
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Ввод некорректен</b>')
        elif int(msg[0]) >= len(args.head_file_name) or int(msg[1]) >= len(args.body_file_name) or \
                int(msg[2]) >= len(args.face_file_name):
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Ввод некорректен</b>')
        else:
            dataBase.set_avatar(message.from_user.id, int(msg[0]), int(msg[1]), int(msg[2]))
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<b>Аватар установлен</b>')
    except Exception as e:
        print(e)
        functions.error_log(e)


@bot.callback_query_handler(func=lambda c: True)  # функция обработки inline кнопок
def func(c):
    """
    :param c:
    :return: None
    """
    try:
        functions.log(c)
        if c.data == '0':
            handler_help(c)
            bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text='<b>Узнать как пользоваться ботом</b>', reply_markup=None)
            bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Ты приемный')
            return
        elif c.data == '1':
            if handler_accept(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Вы начали выполнение задания')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
            return
        elif c.data == '2':
            if handler_cancel(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Вы отказались выполнять '
                                                                                        'задание')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
            return
        elif c.data[1:5] == 'task':
            if handler_task(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Задание отправлено')
                bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id,
                                      text=c.message.text)
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Задание не отправлено')
            return
        elif c.data[1:] == 'give_tsk':
            handler_give_task(c)
            return
        elif c.data[1:7] == 'invite':
            if handler_invite(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Пользователь приглашен')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Приглашение не отправлено')
            return
        elif c.data[1:7] == 'accept':
            """
            
            пофиксить --upd спустя 3 месяца я не помню, что надо было пофиксить
            
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
            return
        elif c.data[2:6] == 'task':
            if handler_corp_task(c):
                user_id = c.data.split('_')
                bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id,
                                      text=c.message.text + '\n------------------\nЗадание отправлено: ' + dataBase.
                                      get_nickname(int(user_id[1][4:])))
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
            return
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
            return
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
            return
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
            return
        elif c.data[1:] == 'corp_members':
            try:
                msg, markup = dataBase.corp_members(c.from_user.id)
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                 text=msg, reply_markup=markup)
            except Exception as e:
                functions.error_log(e)
            return
        elif c.data[1:] == 'get_task':
            try:
                if dataBase.in_corp(c.from_user.id):
                    if dataBase.is_owner(c.from_user.id):
                        dataBase.refresh_corp_tasks(c.from_user.id)
                        msg, markup = dataBase.get_corp_task(c.from_user.id)
                        bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text=msg, reply_markup=markup)
                        return True
                    else:
                        bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                         text='<b>Вы не глава организации</b>')
                        return False
                else:
                    bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                     text='<b>Вы не состоите в организации</b>')
                    return False
            except Exception as e:
                functions.error_log(e)
        elif c.data[1:] == 'get_new_task':
            dataBase.refresh_corp_tasks(c.from_user.id)
            msg, markup = dataBase.get_corp_task(c.from_user.id)
            bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text=msg, reply_markup=markup)
        elif c.data[1:] == 'corp_settings':
            corp_help(c.from_user.id)
            return
        elif c.data[1:] == 'top_rich':
            res = dataBase.get_top('rich')
            bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id, text=res)
            return
        elif c.data[1:] == 'top_orgs':
            res = dataBase.get_top('orgs')
            bot.edit_message_text(parse_mode='HTML', chat_id=c.from_user.id, message_id=c.message.message_id, text=res)
            return
        elif c.data[1:] == 'toorginvite':
            try:
                if dataBase.is_owner(c.from_user.id):
                    msg, markup = dataBase.get_not_in_corp_users(c)
                    bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                     text='<b>Выберете кому отправить приглашение:\n</b>' + msg, reply_markup=markup)
                else:
                    bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                     text='<b>Вы не владелец организации</b>')
                return
            except Exception as e:
                print(e)
                functions.error_log(e)
        elif c.data[1:] == 'change_prof':
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text='<b>Выберите новую профессию</b>')
            dataBase.give_new_prof(c.from_user.id)
            return
        elif c.data[1:] == 'change_spec':
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text=args.test_question)
            dataBase.change_spec(c.from_user.id)
            return
        elif c.data[1:] == 'leave_corp':
            if handler_leave(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Вы покинули орг')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
            return
        elif c.data[1:5] == 'kick':
            if handler_kick(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Пользователь исключен')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
            return
        elif c.data[1:] == 'change_nickname':
            try:
                nickList.append(c.from_user.id)
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text='<b>Введите новый ник:</b>')
            except Exception as e:
                functions.error_log(e)
            return
        elif c.data[1:] == 'crt_avatar':
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text='<b>Выберите параметры аватара:</b>\n'
                                                                             '<i>Head[0-{0}]\nBody[0-{1}]\n'
                                                                             'Face[0-{2}]</i>\n<b>'
                                                                             'формат сообщения "число число число"</b>'.
                             format(len(args.head_file_name) - 1, len(args.body_file_name) - 1,
                                    len(args.face_file_name) - 1))
            avatarList.append(c.from_user.id)
            return
        elif c.data[1:] == 'change_descr':
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text='<i>Введите описание организации:</i>')
            descriptionList.append(c.from_user.id)
            return
        elif c.data[1:] == 'change_nameCorp':
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                             text='<i>Введите новое название организации:</i>')
            nameOfCorpList.append(c.from_user.id)
            return
        elif c.data[1:] == 'crt_org':
            createCorpList.append(c.from_user.id)
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text='<i>Введите название организации:</i>')
            return
        elif c.data[1:] == 'change_owner':
            msg, markup = dataBase.change_owner(c.from_user.id)
            bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                             text=msg, reply_markup=markup)
            return
        elif c.data[1:10] == 'set_owner':
            if handler_set_owner(c):
                bot.answer_callback_query(callback_query_id=c.id, show_alert=False, text='Владелец обновлен')
            else:
                bot.answer_callback_query(callback_query_id=c.id, show_alert=True, text='Нееее, дружок, так не пойдет')
            bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text=c.message.text)
            return
        elif c.data[1:] == 'strt':
            handler_start()
            return
        elif c.data[1:] == 'remove_corp':
            try:
                markup = types.InlineKeyboardMarkup()
                company = dataBase.get_corp(c.from_user.id)
                if company == '0':
                    bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                     text='<b>Вы не состоите в организации</b>')
                    return
                if dataBase.is_owner(c.from_user.id):
                    key1 = types.InlineKeyboardButton('Да', callback_data='/remove_accept')
                    key2 = types.InlineKeyboardButton('Нет', callback_data='/remove_decline')
                    markup.add(key1, key2)
                else:
                    bot.send_message(parse_mode='HTML', chat_id=c.from_user.id,
                                     text='<b>Вы не владелец организации</b>')
                    return
                bot.send_message(parse_mode='HTML', chat_id=c.from_user.id, text='<b>Удалить организацию?</b>',
                                 reply_markup=markup)
            except Exception as e:
                functions.error_log(e)
        elif c.data[1:] == 'ref':
            bot.send_message(chat_id=c.from_user.id, text="Реферальная ссылка для помощи проекту и себе: "
                                                          "https://telegram.me/" + bot.get_me().username + "?start={}"
                             .format(c.from_user.id))
            return
        elif c.data[1:] == 'remove_accept':
            members = dataBase.remove_corp(c.from_user.id)
            for i in members:
                bot.send_message(parse_mode='HTML', chat_id=i, text='<b>Организация расформирована</b>')
                dataBase.upd_corp(i, 0)
            bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text='Организация удалена')
            return
        elif c.data[1:] == 'remove_decline':
            bot.edit_message_text(chat_id=c.from_user.id, message_id=c.message.message_id,
                                  text='Действие отменено')
            return
        elif c.data[1:] == 'log':
            handler_log(c)
            return
        elif c.data[1:] == 'uptime':
            handler_uptime(c)
            return
        elif c.data[1:] == 'errors':
            handler_error(c)
            return
        elif c.data[1:] == 'db':
            handler_db(c)
            return
        elif c.data[1:] == 'exit':
            handler_exit(c)
            return
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['text'])  # функция обработки текстовых сообщений
def handler_text(message):
    """
    :param message: сообщение от пользователя
    :return: None
    """
    try:
        functions.log(message)
        if message.text == args.acceptWorkButton or message.text == args.cancelWorkButton:
            if message.text == args.acceptWorkButton:
                handler_accept(message)
                return
            elif message.text == args.cancelWorkButton:
                handler_cancel(message)
                return
        elif message.text == args.helpButtonName:
            handler_help(message)
            return
        elif message.text == args.AboutMeButtonName:
            handler_me(message)
            return
        elif message.text == args.CorpMenuButtonName:
            handler_corp_menu(message)
            return
        elif message.text == args.TopsButtonName:
            handler_tops(message)
            return
        elif message.text == args.AboutMeButtonName:
            handler_me(message)
            return
        elif message.text == args.AhelpButtonName:
            try:
                if functions.is_admin(message.from_user.id):
                    markup = inline_keyboard(message.from_user.id, False, False, True, False, False)
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<b>Меню администратора</b>\n'
                                          '/a (+сообщение) - Админ чат\n'
                                          '/all (+сообщение) - Сообщение всем\n'
                                          '/change_db - Заменить базу данных\n'
                                          '/add_quest - (по формату /add_quest , профессия , задание , ранг , время)',
                                     reply_markup=markup)
                else:
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='Отказано в доступе')
                return
            except Exception as e:
                functions.error_log(e)
        elif message.text in args.techList or message.text in args.gumList or message.text in args.lowList:
            if dataBase.set_profession(message, False):
                markup = inline_keyboard(message.from_user.id, False, False, False, False, False)
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<i>Ваша профессия</i> <b>' + message.text + '</b>', reply_markup=markup)
                if dataBase.get_nickname(message.from_user.id) == "None":
                    bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                     text='<i>Теперь укажите ваш никнейм </i>')
                    nickList.append(message.from_user.id)
            else:
                bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                                 text='<b>Произошла ошибка, повторите попытку позже</b>')
                return
        elif message.from_user.id in args.new_prof_list:
            dataBase.set_profession(message, functions.in_prof_arr(message.text))
            markup = inline_keyboard(message.from_user.id, False, False, False, False, False)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<i>Ваша новая профессия</i> <b>' + message.text + '</b>', reply_markup=markup)
            return
        elif message.from_user.id in avatarList:
            index = avatarList.index(message.from_user.id)
            set_avatar(message)
            avatarList.pop(index)
            return
        elif message.from_user.id in createCorpList:
            index = createCorpList.index(message.from_user.id)
            handler_create_corp(message)
            createCorpList.pop(index)
            return
        elif message.from_user.id in descriptionList:
            index = descriptionList.index(message.from_user.id)
            handler_set_desc(message)
            descriptionList.pop(index)
            return
        elif message.from_user.id in nameOfCorpList:
            index = nameOfCorpList.index(message.from_user.id)
            handler_set_name(message)
            nameOfCorpList.pop(index)
            return
        elif message.from_user.id in nickList:
            index = nickList.index(message.from_user.id)
            dataBase.set_nickname(message)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id,
                             text='<i>Ваш никнейм</i> <b>' + message.text + '</b>')
            nickList.pop(index)
            return
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
                    return
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
                    return
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
                    return
            else:
                bot.send_message(message.from_user.id, message.text)
                return
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['photo'])
def handler_photo(message):
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе
    """
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['contact'])
def handler_photo(message):
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе
    """
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['sticker'])
def handler_photo(message):
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе (если не админ)
    """
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
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе
    """
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['location'])
def handler_photo(message):
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе
    """
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['audio'])
def handler_photo(message):
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе
    """
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['video'])
def handler_photo(message):
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе
    """
    try:
        functions.wrong_input(message.from_user.id, dataBase.get_spec(message.from_user.id))
    except Exception as e:
        functions.error_log(e)


@bot.message_handler(content_types=['document'])
def handler_photo(message):
    """
    :param message: сообщение от пользователя
    :return: Сообщение о некорректном вводе (если не админ)
    """
    try:
        functions.log(message)
        if functions.is_admin(message.from_user.id):
            args.change_db.pop(args.change_db.index(message.from_user.id))
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open(args.databaseName, 'wb') as file:
                file.write(downloaded_file)
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>База данных заменена</i>')
        else:
            bot.send_message(parse_mode='HTML', chat_id=message.from_user.id, text='<i>Отказано, сука, в доступе</i>')
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

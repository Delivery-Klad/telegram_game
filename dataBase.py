"""
файл для работы с базой данных
"""
# import base64
from telebot import types
import sqlite3
import telebot
import random
import functions
import args


def create_tables():  # создание таблиц в sqlшеу если их нет
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Users(ID INTEGER,'  # телеграм id
                       'UserName TEXT,'         # телеграм username
                       'NickName TEXT,'         # ник(чтобы не палить username телеграма)
                       'Spec TEXT,'             # специализация
                       'Profession TEXT,'       # профессия 
                       'Status TEXT,'           # работает/отдыхает
                       'End_time TEXT,'         # время начала выполнения задания
                       'Count_Works INTEGER,'   # количество выполненных заданий
                       'Reg_Date TEXT,'         # дата регистрации
                       'UserRank INTEGER,'      # ранг пользователя
                       'task TEXT,'             # присутствует ли задание
                       'Money INTEGER,'         # баланс
                       'isOwner INTEGER,'       # является ли владельцем компании
                       'Comp INTEGER,'          # ID компании
                       'TaskNow TEXT,'          # текущее задание
                       'InviteID INTEGER)')     # ID приглосившего человека
        cursor.execute('CREATE TABLE IF NOT EXISTS Quests(Profession TEXT,'  # профессия 
                       'Quest TEXT,'            # задание
                       'Rank INTEGER,'          # ранг/сложность задания
                       'Time INTEGER)')         # время выполнения задания
        cursor.execute('CREATE TABLE IF NOT EXISTS Profs(Prof TEXT,'  # профессия 
                       'ProfCheck INTEGER,'     # 0/1/3 - гум/технарь/доступен всем
                       'ProfRank INTEGER)')     # ранг, с которого доступна профессия
        cursor.execute('CREATE TABLE IF NOT EXISTS Companies(ID INTEGER,'  # уникальный ID 
                       'Name TEXT,'             # название
                       'Description TEXT,'      # описание
                       'CountWorks INTEGER)')   # кол-во выполненных работ
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def set_nickname(nickname):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute(
            "UPDATE Users SET NickName='{0}' WHERE ID='{1}'".format(str(nickname.text), str(nickname.from_user.id)))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def set_profession(message, in_prof_arr):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if message.text in args.techList:
            cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
            spec = cursor.fetchall()
            if spec[0][0] == 'tech':
                cursor.execute(
                    "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text),
                                                                              str(message.from_user.id)))
            else:
                return False
        elif message.text in args.gumList:
            cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
            spec = cursor.fetchall()
            if spec[0][0] == 'gum':
                cursor.execute(
                    "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text),
                                                                              str(message.from_user.id)))
            else:
                return False
        elif in_prof_arr:
            cursor.execute(
                "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text),
                                                                          str(message.from_user.id)))
        else:
            cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
            spec = cursor.fetchall()
            if spec[0][0] == 'low':
                cursor.execute(
                    "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text),
                                                                              str(message.from_user.id)))
            else:
                return False
        connect.commit()
        return True
    except Exception as e:
        functions.error_log(e)


def set_owner(user_id, owner):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET isOwner={0} WHERE ID={1}".format(owner, user_id))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def get_nickname(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT NickName FROM Users WHERE ID=" + str(user_id))
        name = cursor.fetchall()
        return name[0][0]
    except Exception as e:
        functions.error_log(e)


def get_spec(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(user_id))
        spec = cursor.fetchall()
        return spec[0][0]
    except Exception as e:
        functions.error_log(e)


def get_prof(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT Profession FROM Users WHERE ID=" + str(user_id))
    prof = cursor.fetchall()
    return prof[0][0]


def get_user_rank(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT UserRank FROM Users WHERE ID=" + str(user_id))
    rank = cursor.fetchall()
    return rank[0][0]


def get_prof_rank(quest):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT Rank FROM Quest WHERE Quest=" + str(quest))
    rank = cursor.fetchall()[0][0]
    return rank


def get_task(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Quest FROM Quests WHERE Profession='{0}' AND Rank<='{1}'".
                       format(str(get_prof(user_id)), str(get_user_rank(user_id))))
        quests = cursor.fetchall()
        if len(quests) > 1:
            task = random.randint(0, len(quests) - 1)
        else:
            task = 0
        return quests[task][0]
    except Exception as e:
        functions.error_log(e)


def get_corp_task(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Quest,Profession,Rank FROM Quests")
        quests = cursor.fetchall()
        msg = 'Вы можете распределеить задания между своими сотрудниками\n----------\nПрофессия: '
        markup = types.InlineKeyboardMarkup()
        if len(quests) > 1:
            for i in range(5):
                task = random.randint(0, len(quests) - 1)
                if quests[task][1] in args.all_techList:
                    cursor.execute("SELECT MAX(id) FROM CorpTasks")
                    max_id = cursor.fetchall()[0][0]
                    data = [quests[task][0], "tech", quests[task][2], user_id, int(max_id) + 1]
                    cursor.execute("INSERT INTO CorpTasks VALUES (?,?,?,?,?)", data)
                    connect.commit()
                    text = quests[task][1]
                    call = '/give_tech' + str(int(max_id) + 1)
                    key = types.InlineKeyboardButton(text, callback_data=call)
                    markup.add(key)
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: <i>{2}</i>\n----------\n'.format(quests[task][1],
                                                                                                quests[task][2],
                                                                                                quests[task][0])
                elif quests[task][1] in args.all_gumList:
                    cursor.execute("SELECT MAX(id) FROM CorpTasks")
                    max_id = cursor.fetchall()[0][0]
                    data = [quests[task][0], "gum", quests[task][2], user_id, int(max_id) + 1]
                    cursor.execute("INSERT INTO CorpTasks VALUES (?,?,?,?,?)", data)
                    connect.commit()
                    text = quests[task][1]
                    call = '/give_tech' + str(int(max_id) + 1)
                    key = types.InlineKeyboardButton(text, callback_data=call)
                    markup.add(key)
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: <i>{2}</i>\n----------\n'.format(quests[task][1],
                                                                                                quests[task][2],
                                                                                                quests[task][0])
                elif quests[task][1] in args.all_lowList:
                    cursor.execute("SELECT MAX(id) FROM CorpTasks")
                    max_id = cursor.fetchall()[0][0]
                    data = [quests[task][0], "low", quests[task][2], user_id, int(max_id) + 1]
                    cursor.execute("INSERT INTO CorpTasks VALUES (?,?,?,?,?)", data)
                    connect.commit()
                    text = quests[task][1]
                    call = '/give_tech' + str(int(max_id) + 1)
                    key = types.InlineKeyboardButton(text, callback_data=call)
                    markup.add(key)
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: <i>{2}</i>\n----------\n'.format(quests[task][1],
                                                                                                quests[task][2],
                                                                                                quests[task][0])
        msg += 'Выберете кому дать задание'
        return msg, markup
    except Exception as e:
        functions.error_log(e)


def get_tech(user_id, task_id):
    try:
        company = get_corp(user_id)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Profession FROM Quests WHERE Quest=(SELECT Task FROM CorpTasks WHERE id=" +
                       str(task_id) + ")")
        prof = cursor.fetchall()[0][0]
        cursor.execute("SELECT rank FROM CorpTasks WHERE ownerID={0} AND id={1}".format(user_id, task_id))
        rank = cursor.fetchall()[0][0]
        cursor.execute("SELECT NickName,ID,Profession,UserRank FROM Users WHERE UserRank>={0} AND Spec='tech' AND "
                       "Profession='{1}' AND Comp={2} ORDER BY RANDOM() LIMIT 5".format(rank, prof, company))
        users = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        msg = 'Выберете кому дать задание:\n----------\n'
        for i in range(len(users)):
            if int(users[i][1]) != user_id:
                text = str(users[i][0])
                call = '/_task' + str(users[i][1]) + '_' + str(task_id)
                key = types.InlineKeyboardButton(text, callback_data=call)
                markup.add(key)
                msg += str(users[i][0]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3]) + '\n'
        return msg, markup
    except Exception as e:
        functions.error_log(e)
        return 'Выберете кому дать задание:\n----------\nNone'


def get_gum(user_id, task_id):
    try:
        company = get_corp(user_id)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT rank FROM CorpTasks WHERE ownerID={0} AND id={1}".format(user_id, task_id))
        rank = cursor.fetchall()[0][0]
        cursor.execute("SELECT NickName,ID,Profession,UserRank FROM Users WHERE UserRank>={0} AND Spec='gum' AND "
                       "Comp={1} ORDER BY RANDOM() LIMIT 5".format(rank, company))
        users = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        msg = 'Выберете кому дать задание:\n----------\n'
        for i in range(len(users)):
            if int(users[i][1]) != user_id:
                text = str(users[i][0])
                call = '/_task' + str(users[i][1]) + '_' + str(task_id)
                key = types.InlineKeyboardButton(text, callback_data=call)
                markup.add(key)
                msg += str(users[i][0]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3]) + '\n'
        return msg, markup
    except Exception as e:
        functions.error_log(e)
        return 'Выберете кому дать задание:\n----------\nNone'


def get_low(user_id, task_id):
    try:
        company = get_corp(user_id)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT rank FROM CorpTasks WHERE ownerID={0} AND id={1}".format(user_id, task_id))
        rank = cursor.fetchall()[0][0]
        cursor.execute("SELECT NickName,ID,Profession,UserRank FROM Users WHERE UserRank>={0} AND Spec='low' AND "
                       "Comp={1} ORDER BY RANDOM() LIMIT 5".format(rank, company))
        users = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        msg = 'Выберете кому дать задание:\n'
        for i in range(len(users)):
            if int(users[i][1]) != user_id:
                text = str(users[i][0])
                call = '/_task' + str(users[i][1]) + '_' + str(task_id)
                key = types.InlineKeyboardButton(text, callback_data=call)
                markup.add(key)
                msg += str(users[i][0]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3]) + '\n'
        return msg, markup
    except Exception as e:
        functions.error_log(e)
        return 'Выберете кому дать задание:\n----------\nNone'


def get_workers(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID,NickName,Profession,UserRank FROM Users WHERE Status='{0}' ORDER BY RANDOM() LIMIT 5"
                       .format(str(args.waitStatus)))
        users = cursor.fetchall()
        msg_text = ''
        markup = types.InlineKeyboardMarkup()
        for i in range(len(users)):
            if users[i][0] != user_id and int(users[i][0]) != 0:
                call = '/task' + str(users[i][0])
                msg = 'Дать задание  ' + str(users[i][1])
                key = types.InlineKeyboardButton(msg, callback_data=call)
                markup.add(key)
                msg_text += str(users[i][1]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3])
                msg_text += '\n'
        return msg_text, markup
    except Exception as e:
        functions.error_log(e)
        return 'Некому дать задание', None


def get_balance(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Money FROM Users WHERE ID=" + str(user_id))
        money = str(cursor.fetchall()[0][0])
        money += str(args.currency)
        return money
    except Exception as e:
        functions.error_log(e)


def get_owner(company):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID FROM Users WHERE Comp={0} AND isOwner=1".format(str(company)))
    ids = cursor.fetchall()
    ids = ids[0][0]
    return ids


def get_owner_nickname(company):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT NickName FROM Users WHERE Comp={0} AND isOwner=1".format(company))
    name = cursor.fetchall()[0][0]
    return name


def get_task_cost(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT TaskNow FROM Users WHERE ID={0}".format(str(user_id)))
        task = cursor.fetchall()[0][0]
        cursor.execute("SELECT Cost FROM Quests WHERE Quest='{0}'".format(task))
        cost = cursor.fetchall()[0][0]
        return cost
    except Exception as e:
        functions.error_log(e)


def get_job_timer(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT TaskNow FROM Users WHERE ID={0}".format(str(user_id)))
        task = cursor.fetchall()[0][0]
        print(task)
        cursor.execute("SELECT Time FROM Quests WHERE Quest='{0}'".format(task))
        time = cursor.fetchall()[0][0]
        print(time)
        return int(time)
    except Exception as e:
        functions.error_log(e)


def get_corp(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE ID=" + str(user_id))
        corp_id = cursor.fetchall()[0][0]
        return corp_id
    except Exception as e:
        functions.error_log(e)
        return True


def get_corp_name(comp_id):
    try:
        if comp_id == 0:
            return '0'
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Name FROM Companies WHERE ID=" + str(comp_id))
        corp_name = cursor.fetchall()[0][0]
        return corp_name
    except Exception as e:
        functions.error_log(e)
        return True


def get_avatar(ids):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT photo FROM userPhotos WHERE ID=" + str(ids))
        photo = cursor.fetchall()[0][0]
        photo = photo.encode()[2:-1]
        print(photo)
        print(type(photo))
        return photo
    except Exception as e:
        functions.error_log(e)


def get_request(to_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT DISTINCT toUserID,fromWho,type FROM Requests WHERE toUserID={0}".format(to_id))
    res = cursor.fetchall()
    msg = ''
    markup = types.InlineKeyboardMarkup()
    for i in range(len(res)):
        text = 'Вступить в ' + str(res[i][1])
        call = '/accept' + str(get_owner(res[i][1]))
        key = types.InlineKeyboardButton(text, callback_data=call)
        markup.add(key)
        msg += str(i + 1) + ') ' + str(res[i][1])
        msg += '\n'
    return msg, markup


def get_ref_owner(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT InviteID FROM Users WHERE ID=" + str(user_id))
        owner_id = cursor.fetchall()[0][0]
        if len(str(owner_id)) > 1:
            return int(owner_id)
        else:
            return 0
    except Exception as e:
        functions.error_log(e)
        return str('none')


def get_not_in_corp_users(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID,NickName,Profession,UserRank FROM Users WHERE Comp=0 ORDER BY RANDOM() LIMIT 5")
        users = cursor.fetchall()
        msg_text = ''
        markup = types.InlineKeyboardMarkup()
        for i in range(len(users)):
            if users[i][0] != message.from_user.id:
                print(i)
                call = '/invite' + str(users[i][0])
                msg = 'Пригласить  ' + str(users[i][1])
                key = types.InlineKeyboardButton(msg, callback_data=call)
                markup.add(key)
                msg_text += str(users[i][1]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3])
                msg_text += '\n'
        return msg_text, markup
    except Exception as e:
        functions.error_log(e)
        return 'Нет свободных людей', None


def get_members_id(corp_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID FROM Users WHERE Comp={0}".format(corp_id))
        users = cursor.fetchall()
        res = []
        for i in range(len(users)):
            res.append(int(users[i][0]))
        return res
    except Exception as e:
        functions.error_log(e)


def get_top(top):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if top == 'rich':
            cursor.execute("SELECT NickName FROM Users ORDER BY Money DESC LIMIT 10")
            users = cursor.fetchall()
            cursor.execute("SELECT ID FROM Users ORDER BY Money DESC LIMIT 10")
            users_id = cursor.fetchall()
            res = '<b>Топ-10 богачей:</b>'
            for i in range(len(users)):
                res += '\n{}) {}: {}'.format(i + 1, users[i][0], get_balance(int(users_id[i][0])))
            return res
        elif top == 'orgs':
            cursor.execute("SELECT Name FROM Companies ORDER BY CountWorks DESC LIMIT 10")
            orgs = cursor.fetchall()
            res = '<b>Топ-10 организаций:</b>'
            for i in range(len(orgs)):
                res += '\n{}) {}:'.format(i + 1, orgs[i][0])
            return res
    except Exception as e:
        functions.error_log(e)


def add_money(user_id, money):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Money=Money+{0} WHERE ID={1}".format(money, user_id))
        connect.commit()
        upd_task_now(user_id, "None")
        owner_id = get_ref_owner(user_id)
        if str(owner_id) != 'none' and owner_id != 0:
            cursor.execute("UPDATE Users SET Money=Money+{0} WHERE ID={1}".
                           format((money / args.referal_procent), owner_id))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def add_quest(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        data = message.text.split(' , ')
        data.pop(0)
        cursor.execute("INSERT INTO Quests VALUES(?, ?, ?, ?)", data)
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def add_avatar(ids, file):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        data = [ids, r'{}'.format(str(file))]
        cursor.execute("INSERT INTO userPhotos VALUES(?, ?)", data)
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def create_corp(user_id, name):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT MAX(ID) FROM Companies")
        max_id = cursor.fetchall()[0][0] + 1
        data = [max_id, name, 'None', 0]
        cursor.execute("INSERT INTO Companies VALUES(?, ?, ?, ?)", data)
        connect.commit()
        upd_corp(user_id, max_id)
    except Exception as e:
        functions.error_log(e)


def remove_corp(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        corp_id = get_corp(user_id)
        cursor.execute("DELETE FROM Companies WHERE ID={0}".format(corp_id))
        connect.commit()
        set_owner(user_id, 0)
        upd_corp(user_id, 0)
        members = get_members_id(corp_id)
        return members
    except Exception as e:
        functions.error_log(e)


def upd_corp(user_id, company):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Comp={0} WHERE ID={1}".format(company, user_id))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def upd_spec(user_id, spec):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Spec='{0}' WHERE ID={1}".format(spec, str(user_id)))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def upd_can_accept(user_id, check):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET task={0} WHERE ID={1}".format(str(check), str(user_id)))
    connect.commit()


def upd_task_now(user_id, task):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET TaskNow='{0}' WHERE ID={1}".format(str(task), str(user_id)))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def upd_quests():
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM {0}".format("Quests"))
    args.QuestsArr = []
    res = cursor.fetchall()
    for i in res:
        args.QuestsArr.append([i[0], i[1], i[2], i[3]])


def upd_prof():  # Обновление полного списка профессий и профессий для начинающих
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Profs")
    args.ProfArr = cursor.fetchall()

    args.techList = []
    args.gumList = []
    low_prof_rank = 0
    gum_id = 0
    tech_id = 1

    for i in args.ProfArr:
        if i[2] == low_prof_rank and i[1] == tech_id:  # Заполнение techList профессиями
            args.techList.append(i[0])
        elif i[2] == low_prof_rank and i[1] == gum_id:  # Заполнение gumList профессиями
            args.gumList.append(i[0])
        elif i[2] == low_prof_rank and i[1] == 3:
            args.lowList.append(i[0])

    for i in args.ProfArr:
        if i[1] == tech_id:
            args.all_techList.append(i[0])
        elif i[1] == gum_id:
            args.all_gumList.append(i[0])
        elif i[1] == 3:
            args.all_lowList.append(i[0])


def in_corp(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE ID=" + str(user_id))
        corp_name = int(cursor.fetchall()[0][0])
        if corp_name == 0:
            return False
        else:
            return True
    except Exception as e:
        functions.error_log(e)
        return True


def is_owner(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE isOwner=1 AND ID=" + str(user_id))
        res = cursor.fetchall()[0][0]
        return True
    except Exception as e:
        functions.error_log(e)
        return False


def is_free(user_id):  # проверить выполняет ли пользователь какую-либо работу
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Status FROM Users WHERE ID=" + str(user_id))
        status = cursor.fetchall()
        if status[0][0] == args.waitStatus:
            return True
        else:
            return False
    except Exception as e:
        functions.error_log(e)


def give_corp_task(task_id, user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Task,spec,rank FROM CorpTasks WHERE id=" + str(task_id))
        task = cursor.fetchall()
        if get_user_rank(user_id) >= int(task[0][2]) and get_spec(user_id) == task[0][1]:
            upd_task_now(user_id, task[0][0])
        cursor.execute("DELETE FROM CorpTasks WHERE id=" + str(task_id))
        connect.commit()
        msg = '<b>Вы получили задание от главы организиции:</b> ' + task[0][0]
        return msg
    except Exception as e:
        functions.error_log(e)
        return 'None'


def kick_from_corp(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Comp=0 WHERE ID={0}".format(user_id))
    connect.commit()


def corp_members(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    markup = types.InlineKeyboardMarkup()
    if get_corp(user_id) == 0:
        call = '/me'
        key = types.InlineKeyboardButton('/me', callback_data=call)
        markup.add(key)
        return 'Вы не состоите в организации', markup
    cursor.execute("SELECT ID,NickName,Profession,UserRank FROM Users WHERE Comp={0}".
                   format(get_corp(user_id)))
    members = cursor.fetchall()
    msg = '<b>Члены организации:</b>\n'
    for i in range(len(members)):
        if user_id != members[i][0]:
            text = 'Выгнать ' + str(members[i][1])
            call = '/kick' + str(members[i][0])
            key = types.InlineKeyboardButton(text, callback_data=call)
            markup.add(key)
        msg += '<b>' + str(members[i][1]) + '</b> <i>' + str(members[i][2]) + ' Ранг: ' + str(members[i][3]) + '</i>'
        msg += '\n'
    return msg, markup


def change_owner(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    markup = types.InlineKeyboardMarkup()
    if get_corp(user_id) == 0:
        call = '/me'
        key = types.InlineKeyboardButton('/me', callback_data=call)
        markup.add(key)
        return 'Вы не состоите в организации', markup
    cursor.execute("SELECT ID,NickName,Profession,UserRank FROM Users WHERE Comp={0}".
                   format(get_corp(user_id)))
    members = cursor.fetchall()
    msg = '<b>Члены организации:</b>\n'
    for i in range(len(members)):
        if user_id != members[i][0]:
            text = 'Назначить ' + str(members[i][1])
            call = '/set_owner' + str(members[i][0])
            key = types.InlineKeyboardButton(text, callback_data=call)
            markup.add(key)
        msg += '<b>' + str(members[i][1]) + '</b> <i>' + str(members[i][2]) + ' Ранг: ' + str(members[i][3]) + '</i>'
        msg += '\n'
    return msg, markup


def corp_info(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        corp_id = get_corp(user_id)
        cursor.execute("SELECT Description FROM Companies WHERE ID={0}".format(corp_id))
        desc = cursor.fetchall()[0][0]
        cursor.execute("SELECT Name FROM Companies WHERE ID={0}".format(corp_id))
        company = cursor.fetchall()[0][0]
        owner = get_owner_nickname(corp_id)
        msg = '<b>Название:</b> <i>{0}</i>\n<b>Владелец:</b> <i>{1}</i>\n<b>Описание:</b> <i>{2}</i>'.format(
            company, owner, desc)
        return msg
    except Exception as e:
        msg = 'Вы не владелец организации'
        functions.error_log(e)
        return msg


def update_corp_description(user_id, name):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if is_owner(user_id):
            cursor.execute("UPDATE Companies SET Description='{0}' WHERE ID={1}".format(name, get_corp(user_id)))
            connect.commit()
            return 'Описание обновлено'
        else:
            return 'Вы не владелец организации'
    except Exception as e:
        functions.error_log(e)


def update_corp_name(user_id, name):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if is_owner(user_id):
            cursor.execute("UPDATE Companies SET Name='{0}' WHERE ID={1}".format(name, get_corp(user_id)))
            connect.commit()
            return 'Название обновлено'
        else:
            return 'Вы не владелец организации'
    except Exception as e:
        functions.error_log(e)


def leave_corp(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if not is_owner(user_id):
            cursor.execute("UPDATE Users SET Comp=0 WHERE ID={0}".format(user_id))
            connect.commit()
            return True
        else:
            return False
    except Exception as e:
        functions.error_log(e)


def can_accept(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT task FROM Users WHERE ID=" + str(user_id))
    can = cursor.fetchall()
    if can[0][0] == "1":
        upd_can_accept(user_id, 0)
        return True
    else:
        return False


def up_lvl(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Count_Works FROM Users WHERE ID=" + str(user_id))
        jobs = cursor.fetchall()
        if jobs[0][0] in args.jobs_to_lvl_up:
            cursor.execute("UPDATE Users SET UserRank=UserRank+1 WHERE ID=" + str(user_id))
            give_new_prof(user_id)
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def give_new_prof(user_id):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(user_id))
        prof_id = cursor.fetchall()
        prof_id = prof_id[0][0]
        if prof_id == 'low':
            prof_id = 3
        elif prof_id == 'gym':
            prof_id = 0
        else:
            prof_id = 1
        cursor.execute("SELECT Prof FROM Profs WHERE ProfRank<={0} AND ProfCheck={1}".
                       format(str(get_user_rank(user_id)), prof_id))
        profs = cursor.fetchall()
        for i in range(len(profs)):
            print(i)
            user_markup.row(profs[i][0])
        args.bot.send_message(parse_mode='HTML', chat_id=user_id,
                              text='<i>У вас появилась возможность выбрать новую профессию</i>',
                              reply_markup=user_markup)
        args.new_prof_list.append(user_id)
    except Exception as e:
        functions.error_log(e)


def start_job(user_id, status, time):  # замена статуса и указание времени начала
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Status='{0}' WHERE ID='{1}'".format(str(status), str(user_id)))
        cursor.execute("UPDATE Users SET End_time='{0}' WHERE ID='{1}'".format(str(time), str(user_id)))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def plus_count_works(user_id):  # указание количества выполненных работ
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Count_Works=Count_Works+1 WHERE ID='{0}'".format(str(user_id)))
        connect.commit()
        up_lvl(user_id)  # повышение ранга
    except Exception as e:
        functions.error_log(e)


def minus_money(user_id, money):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Money=Money-{0} WHERE ID='{1}'".format(money, user_id))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def check_requests(user_id, company):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT toUserID,fromWho FROM Requests")
    reqs = cursor.fetchall()
    print(reqs)
    print(len(reqs))
    for i in range(len(reqs)):
        if reqs[i][0] == user_id and reqs[i][1] == company:
            return False
    return True


def new_req(to_id, from_who):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Requests VALUES ({0},'{1}',0)".format(to_id, from_who))
    connect.commit()
    get_request(to_id)


def delete_request(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("DELETE FROM Requests WHERE toUserID={0}".format(user_id))
    connect.commit()


def refresh_corp_tasks(user_id):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("DELETE FROM CorpTasks WHERE ownerID={0}".format(user_id))
        connect.commit()
    except Exception as e:
        functions.error_log(e)


def change_spec(user_id):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Spec='None',Profession='None',Count_Works=0,Status='{0}',"
                   "End_time='None',UserRank=0 WHERE ID={1}".format(str(args.waitStatus), str(user_id)))
    connect.commit()

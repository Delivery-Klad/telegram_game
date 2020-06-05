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


def createTables():  # создание таблиц в sql если их нет
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS Users(ID INTEGER,'  # телеграм id
                       'UserName TEXT,'  # телеграм username
                       'NickName TEXT,'  # ник(чтобы не палить username телеграма)
                       'Spec TEXT,'  # специализация
                       'Profession TEXT,'  # профессия 
                       'Status TEXT,'  # работает/отдыхает
                       'End_time TEXT,'  # время начала выполнения задания
                       'Count_Works INTEGER,'  # количество выполненных заданий
                       'Reg_Date TEXT,'
                       'UserRank TEXT,'
                       'Comp TEXT,'
                       'CompDiscription TEXT,'
                       'task TEXT)')  # дата регистрации
        cursor.execute('CREATE TABLE IF NOT EXISTS Quests(Profession TEXT,'  # профессия 
                       'Quest TEXT,'  # задание
                       'Rank INTEGER,'  # ранг/сложность задания
                       'Time INTEGER)')  # время выполнения задания
        cursor.execute('CREATE TABLE IF NOT EXISTS Profs(Prof TEXT,'  # профессия 
                       'ProfCheck INTEGER,'
                       'ProfRank INTEGER)')  # 0/1/3 - гум/технарь/доступен всем
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('createTables')


def set_nickname(nickName):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute(
            "UPDATE Users SET NickName='{0}' WHERE ID='{1}'".format(str(nickName.text), str(nickName.from_user.id)))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('set_nickname')


def set_profession(message, in_profArr):
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
        elif in_profArr:
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
        createTables()
        functions.errorLog('set_professoin')


def setOwner(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET isOwner=1 WHERE ID={0}".format(str(userID)))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('setOwner')


def get_nickname(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT NickName FROM Users WHERE ID=" + str(userID))
        name = cursor.fetchall()
        return name[0][0]
    except Exception as e:
        createTables()
        functions.errorLog('get_nickname')


def get_spec(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(userID))
        spec = cursor.fetchall()
        return spec[0][0]
    except Exception as e:
        createTables()
        functions.errorLog('get_spec')


def get_prof(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT Profession FROM Users WHERE ID=" + str(userID))
    prof = cursor.fetchall()
    return prof[0][0]


def get_userRank(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT UserRank FROM Users WHERE ID=" + str(userID))
    rank = cursor.fetchall()
    return rank[0][0]


def get_profRank(quest):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT Rank FROM Quest WHERE Quest=" + str(quest))
    rank = cursor.fetchall()[0][0]
    return rank


def get_task(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Quest FROM Quests WHERE Profession='{0}' AND Rank<='{1}'".
                       format(str(get_prof(userID)), str(get_userRank(userID))))
        quests = cursor.fetchall()
        if len(quests) > 1:
            task = random.randint(0, len(quests) - 1)
        else:
            task = 0
        return quests[task][0]
    except Exception as e:
        createTables()
        functions.errorLog('get_task')


def get_corpTask(userID):
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
                    maxID = cursor.fetchall()[0][0]
                    data = [quests[task][0], "tech", quests[task][2], userID, int(maxID) + 1]
                    cursor.execute("INSERT INTO CorpTasks VALUES (?,?,?,?,?)", data)
                    connect.commit()
                    text = quests[task][1]
                    call = '/give_tech' + str(int(maxID) + 1)
                    key = types.InlineKeyboardButton(text, callback_data=call)
                    markup.add(key)
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: <i>{2}</i>\n----------\n'.format(quests[task][1],
                                                                                                quests[task][2],
                                                                                                quests[task][0])
                elif quests[task][1] in args.all_gumList:
                    cursor.execute("SELECT MAX(id) FROM CorpTasks")
                    maxID = cursor.fetchall()[0][0]
                    data = [quests[task][0], "gum", quests[task][2], userID, int(maxID) + 1]
                    cursor.execute("INSERT INTO CorpTasks VALUES (?,?,?,?,?)", data)
                    connect.commit()
                    text = quests[task][1]
                    call = '/give_tech' + str(int(maxID) + 1)
                    key = types.InlineKeyboardButton(text, callback_data=call)
                    markup.add(key)
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: <i>{2}</i>\n----------\n'.format(quests[task][1],
                                                                                                quests[task][2],
                                                                                                quests[task][0])
                elif quests[task][1] in args.all_lowList:
                    cursor.execute("SELECT MAX(id) FROM CorpTasks")
                    maxID = cursor.fetchall()[0][0]
                    data = [quests[task][0], "low", quests[task][2], userID, int(maxID) + 1]
                    cursor.execute("INSERT INTO CorpTasks VALUES (?,?,?,?,?)", data)
                    connect.commit()
                    text = quests[task][1]
                    call = '/give_tech' + str(int(maxID) + 1)
                    key = types.InlineKeyboardButton(text, callback_data=call)
                    markup.add(key)
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: <i>{2}</i>\n----------\n'.format(quests[task][1],
                                                                                                quests[task][2],
                                                                                                quests[task][0])
        msg += 'Выберете кому дать задание'
        return msg, markup
    except Exception as e:
        createTables()
        functions.errorLog('get_CorpTask')


def get_tech(userID, taskID):
    try:
        company = get_company(userID)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Profession FROM Quests WHERE Quest=(SELECT Task FROM CorpTasks WHERE id=" +
                       str(taskID) + ")")
        prof = cursor.fetchall()[0][0]
        cursor.execute("SELECT rank FROM CorpTasks WHERE ownerID={0} AND id={1}".format(userID, taskID))
        rank = cursor.fetchall()[0][0]
        cursor.execute("SELECT NickName,ID,Profession,UserRank FROM Users WHERE UserRank>={0} AND Spec='tech' AND "
                       "Profession='{1}' AND Comp='{2}' ORDER BY RANDOM() LIMIT 5".format(rank, prof, company))
        users = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        msg = 'Выберете кому дать задание:\n----------\n'
        for i in range(len(users)):
            if int(users[i][1]) != userID:
                text = str(users[i][0])
                call = '/_task' + str(users[i][1]) + '_' + str(taskID)
                key = types.InlineKeyboardButton(text, callback_data=call)
                markup.add(key)
                msg += str(users[i][0]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3]) + '\n'
        return msg, markup
    except Exception as e:
        createTables()
        functions.errorLog('get_tech')
        return 'Выберете кому дать задание:\n----------\nNone'


def get_gum(userID, taskID):
    try:
        company = get_company(userID)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT rank FROM CorpTasks WHERE ownerID={0} AND id={1}".format(userID, taskID))
        rank = cursor.fetchall()[0][0]
        cursor.execute("SELECT NickName,ID,Profession,UserRank FROM Users WHERE UserRank>={0} AND Spec='gum' AND "
                       "Comp='{1}' ORDER BY RANDOM() LIMIT 5".format(rank, company))
        users = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        msg = 'Выберете кому дать задание:\n----------\n'
        for i in range(len(users)):
            if int(users[i][1]) != userID:
                text = str(users[i][0])
                call = '/_task' + str(users[i][1]) + '_' + str(taskID)
                key = types.InlineKeyboardButton(text, callback_data=call)
                markup.add(key)
                msg += str(users[i][0]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3]) + '\n'
        return msg, markup
    except Exception as e:
        createTables()
        functions.errorLog('get_gum')
        return 'Выберете кому дать задание:\n----------\nNone'


def get_low(userID, taskID):
    try:
        company = get_company(userID)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT rank FROM CorpTasks WHERE ownerID={0} AND id={1}".format(userID, taskID))
        rank = cursor.fetchall()[0][0]
        cursor.execute("SELECT NickName,ID,Profession,UserRank FROM Users WHERE UserRank>={0} AND Spec='low' AND "
                       "Comp='{1}' ORDER BY RANDOM() LIMIT 5".format(rank, company))
        users = cursor.fetchall()
        markup = types.InlineKeyboardMarkup()
        msg = 'Выберете кому дать задание:\n'
        for i in range(len(users)):
            if int(users[i][1]) != userID:
                text = str(users[i][0])
                call = '/_task' + str(users[i][1]) + '_' + str(taskID)
                key = types.InlineKeyboardButton(text, callback_data=call)
                markup.add(key)
                msg += str(users[i][0]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3]) + '\n'
        return msg, markup
    except Exception as e:
        createTables()
        functions.errorLog('get_low')
        return 'Выберете кому дать задание:\n----------\nNone'


def get_workers(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID,NickName,Profession,UserRank FROM Users WHERE Status='{0}' ORDER BY RANDOM() LIMIT 5"
                       .format(str(args.waitStatus)))
        users = cursor.fetchall()
        msg_text = ''
        markup = types.InlineKeyboardMarkup()
        for i in range(len(users)):
            if users[i][0] != message.from_user.id:
                print(i)
                call = '/task' + str(users[i][0])
                msg = 'Дать задание  ' + str(users[i][1])
                key = types.InlineKeyboardButton(msg, callback_data=call)
                markup.add(key)
                msg_text += str(users[i][1]) + ' ' + str(users[i][2]) + ' Ранг: ' + str(users[i][3])
                msg_text += '\n'
        return msg_text, markup
    except IndexError:
        createTables()
        functions.errorLog('get_workers')
        return 'Некому дать задание', None


def get_balance(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Money FROM Users WHERE ID=" + str(userID))
        money = str(cursor.fetchall()[0][0])
        money += str(args.currency)
        return money
    except Exception as e:
        createTables()
        functions.errorLog('get_balance')


def get_company(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT Comp FROM Users WHERE ID=" + str(userID))
    corpName = cursor.fetchall()[0][0]
    return corpName


def get_owner(company):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID FROM Users WHERE Comp='{0}' AND isOwner=1".format(str(company)))
    ID = cursor.fetchall()
    ID = ID[0][0]
    return ID


def get_taskCost(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT TaskNow FROM Users WHERE ID={0}".format(str(userID)))
        task = cursor.fetchall()[0][0]
        cursor.execute("SELECT Cost FROM Quests WHERE Quest='{0}'".format(task))
        cost = cursor.fetchall()[0][0]
        return cost
    except Exception as e:
        createTables()
        functions.errorLog('get_taskCost')


def get_job_timer(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT TaskNow FROM Users WHERE ID={0}".format(str(userID)))
        task = cursor.fetchall()[0][0]
        print(task)
        cursor.execute("SELECT Time FROM Quests WHERE Quest='{0}'".format(task))
        time = cursor.fetchall()[0][0]
        print(time)
        return int(time)
    except Exception as e:
        createTables()
        functions.errorLog('get_job_timer')


def get_Corp(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE ID=" + str(userID))
        corpName = cursor.fetchall()[0][0]
        return corpName
    except Exception as e:
        createTables()
        functions.errorLog('get_Corp')
        return True


def getAvatar(ID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT photo FROM userPhotos WHERE ID=" + str(ID))
        photo = cursor.fetchall()[0][0]
        photo = photo.encode()[2:-1]
        print(photo)
        print(type(photo))
        return photo
    except Exception as e:
        createTables()
        functions.errorLog('getAvatar')


def getReq(toID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT DISTINCT toUserID,fromWho,type FROM Requests WHERE toUserID={0}".format(toID))
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


def get_refOwner(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT InviteID FROM Users WHERE ID=" + str(userID))
        ownerID = cursor.fetchall()[0][0]
        if len(str(ownerID)) > 1:
            return int(ownerID)
        else:
            return 0
    except Exception as e:
        createTables()
        functions.errorLog('get_refOwner')
        return str('none')


def get_noInCorpUsers(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID,NickName,Profession,UserRank FROM Users WHERE Comp='0' ORDER BY RANDOM() LIMIT 5")
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
    except IndexError:
        createTables()
        functions.errorLog('get_notInCorpUsers')
        return 'Нет свободных людей', None


def add_money(userID, money):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Money=Money+{0} WHERE ID={1}".format(money, userID))
        connect.commit()
        upd_taskNow(userID, "None")
        ownerID = get_refOwner(userID)
        if str(ownerID) != 'none' and ownerID != 0:
            cursor.execute("UPDATE Users SET Money=Money+{0} WHERE ID={1}".
                           format((money / args.referal_procent), ownerID))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('add_money')


def add_Quest(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        data = message.text.split(' , ')
        data.pop(0)
        cursor.execute("INSERT INTO Quests VALUES(?, ?, ?, ?)", data)
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('add_quest')


def addAvatar(ID, file):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        data = [ID, r'{}'.format(str(file))]
        cursor.execute("INSERT INTO userPhotos VALUES(?, ?)", data)
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('addAvatar')


def upd_corp(userID, company):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Comp='{0}' WHERE ID={1}".format(str(company), str(userID)))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('upd_corp')


def upd_spec(userID, spec):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Spec='{0}' WHERE ID={1}".format(spec, str(userID)))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('upd_spec')


def upd_can_accept(userID, check):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET task={0} WHERE ID={1}".format(str(check), str(userID)))
    connect.commit()


def upd_taskNow(userID, task):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET TaskNow='{0}' WHERE ID={1}".format(str(task), str(userID)))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('upd_taskNow')


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
    LowProfRank = 0
    gumID = 0
    techID = 1

    for i in args.ProfArr:
        if i[2] == LowProfRank and i[1] == techID:  # Заполнение techList профессиями
            args.techList.append(i[0])
        elif i[2] == LowProfRank and i[1] == gumID:  # Заполнение gumList профессиями
            args.gumList.append(i[0])
        elif i[2] == LowProfRank and i[1] == 3:
            args.lowList.append(i[0])

    for i in args.ProfArr:
        if i[1] == techID:
            args.all_techList.append(i[0])
        elif i[1] == gumID:
            args.all_gumList.append(i[0])
        elif i[1] == 3:
            args.all_lowList.append(i[0])


def inCorp(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE ID=" + str(userID))
        corpName = cursor.fetchall()[0][0]
        if corpName == "0":
            print('0')
            return False
        else:
            return True
    except Exception as e:
        createTables()
        functions.errorLog('inCorp')
        return True


def isOwner(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE isOwner=1 AND ID=" + str(userID))
        corpName = cursor.fetchall()[0][0]
        return True
    except Exception as e:
        createTables()
        functions.errorLog('isOwner')
        return False


def isFree(userID):  # проверить выполняет ли пользователь какую-либо работу
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Status FROM Users WHERE ID=" + str(userID))
        status = cursor.fetchall()
        if status[0][0] == args.waitStatus:
            return True
        else:
            return False
    except Exception as e:
        createTables()
        functions.errorLog('isFree')


def give_corp_task(taskID, userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Task,spec,rank FROM CorpTasks WHERE id=" + str(taskID))
        task = cursor.fetchall()
        if get_userRank(userID) >= int(task[0][2]) and get_spec(userID) == task[0][1]:
            upd_taskNow(userID, task[0][0])
        cursor.execute("DELETE FROM CorpTasks WHERE id=" + str(taskID))
        connect.commit()
        msg = '<b>Вы получили задание от главы организиции:</b> ' + task[0][0]
        return msg
    except Exception as e:
        createTables()
        functions.errorLog('give_corp_task')
        return 'None'


def kick_from_corp(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Comp='0' WHERE ID={0}".format(str(userID)))
    connect.commit()


def corp_members(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    markup = types.InlineKeyboardMarkup()
    if get_company(userID) == 0:
        call = '/me'
        key = types.InlineKeyboardButton('/me', callback_data=call)
        markup.add(key)
        return 'Вы не состоите в организации', markup
    cursor.execute("SELECT ID,NickName,Profession,UserRank FROM Users WHERE Comp='{0}'".
                   format(str(get_company(userID))))
    members = cursor.fetchall()
    msg = '<b>Члены организации:</b>\n'
    for i in range(len(members)):
        if userID != members[i][0]:
            text = 'Выгнать ' + str(members[i][1])
            call = '/kick' + str(members[i][0])
            key = types.InlineKeyboardButton(text, callback_data=call)
            markup.add(key)
        msg += '<b>' + str(members[i][1]) + '</b> <i>' + str(members[i][2]) + ' Ранг: ' + str(members[i][3]) + '</i>'
        msg += '\n'
    return msg, markup


def corp_info(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT CompDiscription FROM Users WHERE ID={0}".format(str(userID)))
        res = cursor.fetchall()
        company = get_Corp(userID)
        owner = get_owner(company)
        msg = '<b>Название:</b> <i>{0}</i>\n<b>Владелец:</b> <i>{1}</i>\n<b>Описание:</b> <i>{2}</i>'.format(company, owner, res[0][0])
        return msg
    except Exception as e:
        functions.errorLog('corp_info')


def update_corp_description(userID, name):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if isOwner(userID):
            cursor.execute("UPDATE Users SET CompDiscription='{0}' WHERE Comp='{1}'".format(name, get_Corp(userID)))
            connect.commit()
            return 'Описание обновлено'
        else:
            return 'Вы не владелец организации'
    except Exception as e:
        functions.errorLog('update_corp_description')


def leave_corp(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if not isOwner(userID):
            cursor.execute("UPDATE Users SET Comp='0' WHERE ID={0}".format(str(userID)))
            cursor.execute("UPDATE Users SET CompDiscription=None WHERE ID={0}".format(str(userID)))
            connect.commit()
            return True
        else:
            return False
    except Exception as e:
        createTables()
        functions.errorLog('leave_corp')


def can_accept(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT task FROM Users WHERE ID=" + str(userID))
    can = cursor.fetchall()
    if can[0][0] == "1":
        upd_can_accept(userID, 0)
        return True
    else:
        return False


def up_lvl(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Count_Works FROM Users WHERE ID=" + str(userID))
        jobs = cursor.fetchall()
        if jobs[0][0] in args.jobs_to_lvl_up:
            cursor.execute("UPDATE Users SET UserRank=UserRank+1 WHERE ID=" + str(userID))
            give_new_prof(userID)
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('up_lvl')


def give_new_prof(userID):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(userID))
        profID = cursor.fetchall()
        profID = profID[0][0]
        if profID == 'low':
            profID = 3
        elif profID == 'gym':
            profID = 0
        else:
            profID = 1
        cursor.execute("SELECT Prof FROM Profs WHERE ProfRank<={0} AND ProfCheck={1}".
                       format(str(get_userRank(userID)), profID))
        profs = cursor.fetchall()
        for i in range(len(profs)):
            print(i)
            user_markup.row(profs[i][0])
        args.bot.send_message(parse_mode='HTML', chat_id=userID,
                              text='<i>Вы получили новый ранг, теперь вы можете выбрать новую профессию</i>',
                              reply_markup=user_markup)
        args.new_frof_list.append(userID)
    except Exception as e:
        createTables()
        functions.errorLog('gevi_new_prof')


def start_job(userID, status, time):  # замена статуса и указание времени начала
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Status='{0}' WHERE ID='{1}'".format(str(status), str(userID)))
        cursor.execute("UPDATE Users SET End_time='{0}' WHERE ID='{1}'".format(str(time), str(userID)))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('start_job')


def plus_count_works(userID):  # указание количества выполненных работ
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Count_Works=Count_Works+1 WHERE ID='{0}'".format(str(userID)))
        connect.commit()
        up_lvl(userID)  # повышение ранга
    except Exception as e:
        createTables()
        functions.errorLog('plus_count_works')


def minus_money(userID, money):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Money=Money-{0} WHERE ID='{1}'".format(money, userID))
        connect.commit()
    except Exception as e:
        createTables()
        functions.errorLog('minus_money')


def check_requests(userID, company):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT toUserID,fromWho FROM Requests")
    reqs = cursor.fetchall()
    print(reqs)
    print(len(reqs))
    for i in range(len(reqs)):
        if reqs[i][0] == userID and reqs[i][1] == company:
            return False
    return True


def newReq(toID, fromWho):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("INSERT INTO Requests VALUES ({0},'{1}',0)".format(toID, str(fromWho)))
    connect.commit()
    getReq(toID)


def delete_request(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("DELETE FROM Requests WHERE toUserID={0}".format(userID))
    connect.commit()


def refreshCorpTasks(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("DELETE FROM CorpTasks WHERE ownerID={0}".format(userID))
        connect.commit()
    except Exception as e:
        functions.errorLog('refreshCorpTasks')


def change_spec(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Spec='None',Profession='None',Count_Works='0',Status='{0}',End_time='None',"
                   "UserRank='0' WHERE ID={1}".format(str(args.waitStatus), str(userID)))
    connect.commit()

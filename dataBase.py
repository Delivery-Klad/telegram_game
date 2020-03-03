"""
файл для работы с базой данных
"""
import sqlite3
import telebot
import random
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
        print(e)


def set_nickname(nickName):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute(
            "UPDATE Users SET NickName='{0}' WHERE ID='{1}'".format(str(nickName.text), str(nickName.from_user.id)))
        connect.commit()
    except Exception as e:
        print(e)


def set_profession(message, in_profArr):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if message.text in args.techList:
            cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
            spec = cursor.fetchall()
            if spec[0][0] == 'tech':
                cursor.execute(
<<<<<<< HEAD
                    "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text),str(message.from_user.id)))
            else:
                return False
=======
                    "UPDATE Users SET Profession='{0}' WHERE ID='{1}'".format(str(message.text),
                                                                              str(message.from_user.id)))
            
>>>>>>> 9a196c6dc789b9f49afef43b6786018af5517049
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
        print(e)


def setOwner(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET isOwner=1 WHERE ID={0}".format(str(userID)))
        connect.commit()
    except Exception as e:
        print(e)


def get_nickname(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT NickName FROM Users WHERE ID=" + str(userID))
        name = cursor.fetchall()
        return name[0][0]
    except Exception as e:
        print(e)


def get_spec(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(userID))
        spec = cursor.fetchall()
        return spec[0][0]
    except Exception as e:
        print(e)


def get_prof(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT Profession FROM Users WHERE ID=" + str(userID))
    prof = cursor.fetchall()
    print(prof[0][0])
    return prof[0][0]


def get_userRank(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT UserRank FROM Users WHERE ID=" + str(userID))
    rank = cursor.fetchall()
    print(rank[0][0])
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
            task = random.randint(0, len(quests)-1)
        else:
            task = 0
        print(quests[task][0])
        return quests[task][0]
    except Exception as e:
        print(e)


def get_corpTask(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Quest,Profession,Rank FROM Quests")
        quests = cursor.fetchall()
        msg = 'Вы можете распределеить задания между своими сотрудниками\nПрофессия: '
        if len(quests) > 1:
            for i in range(5):
                task = random.randint(0, len(quests)-1)
                print('00')
                if quests[task][1] in args.all_techList:
                    print('1')
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: {2} /give_tech\n'.format(quests[task][1], quests[task][2], quests[task][0])
                elif quests[task][1] in args.all_gumList:
                    print('2')
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: {2} /give_gum\n'.format(quests[task][1], quests[task][2], quests[task][0])
                elif quests[task][1] in args.all_lowList:
                    print('3')
                    msg += '{0}\nТребуемый ранг: {1}\nЗадание: {2} /give_low\n'.format(quests[task][1], quests[task][2], quests[task][0])
        print(msg)
        return msg
    except Exception as e:
        print(e)


def get_workers(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID,NickName,Profession FROM Users WHERE Status='{0}' ORDER BY RANDOM() LIMIT 7"
                       .format(str(args.waitStatus)))
        users = cursor.fetchall()
        msg_text = ''
        print('check')
        print(len(users[0]))
        print(len(users))
        for i in range(len(users)):
            if users[i][0] != message.from_user.id:
                print(i)
                msg_text += str(users[i][1]) + ' ' + str(users[i][2]) + ' /task' + str(users[i][0])
                msg_text += '\n'
        return msg_text
    except Exception as e:
        print(e)


def get_balance(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Money FROM Users WHERE ID=" + str(userID))
        money = str(cursor.fetchall()[0][0])
        money += str(args.currency)
        return money
    except Exception as e:
        print(e)


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
        print(e)


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
        print(e)


def get_Corp(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE ID=" + str(userID))
        corpName = cursor.fetchall()[0][0]
        return corpName
    except Exception as e:
        print(e)
        return True


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
        print(e)
        return True


def kick_from_corp(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Comp='0' WHERE ID={0}".format(str(userID)))
    connect.commit()


def corp_members(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT ID,NickName FROM Users WHERE Comp='{0}'".format(str(get_company(userID))))
    members = cursor.fetchall()
    print(len(members))
    print(members)
    msg = ''
    for i in range(len(members)):
        msg += '<i>' + str(members[i][1]) + '</i>  /kick' + str(members[i][0])
        msg += '\n'
    return msg


def leave_corp(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        if not isOwner(userID):
            cursor.execute("UPDATE Users SET Comp='0' WHERE ID={0}".format(str(userID)))
            connect.commit()
            return True
        else:
            return False
    except Exception as e:
        print(e)


def isOwner(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Comp FROM Users WHERE isOwner=1 AND ID=" + str(userID))
        corpName = cursor.fetchall()[0][0]
        print(corpName)
        return True
    except Exception as e:
        print(e)
        return False


def upd_corp(userID, company):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Comp='{0}' WHERE ID={1}".format(str(company), str(userID)))
        connect.commit()
    except Exception as e:
        print(e)


def upd_spec(userID, spec):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Spec='{0}' WHERE ID={1}".format(spec, str(userID)))
        connect.commit()
    except Exception as e:
        print(e)


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
        print(e)


def change_spec(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Spec='None',Profession='None',Count_Works='0',Status='{0}',End_time='None',"
                   "UserRank='0' WHERE ID={1}".format(str(args.waitStatus), str(userID)))
    connect.commit()


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
        print(e)


def add_money(userID, money):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Money=Money+{0} WHERE ID={1}".format(money, userID))
        connect.commit()
        upd_taskNow(userID, "None")
        ownerID = get_referal_owner(userID)
        if str(ownerID) != 'none' and ownerID != 0:
            cursor.execute("UPDATE Users SET Money=Money+{0} WHERE ID={1}".
                           format((money/args.referal_procent), ownerID))
        connect.commit()
    except Exception as e:
        print(e)


def add_Quest(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        data = message.text.split(' , ')
        data.pop(0)
        print(data)
        cursor.execute("INSERT INTO Quests VALUES(?, ?, ?, ?)", data)
        connect.commit()
    except Exception as e:
        print(e)


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
        print(e)


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
        print(profs)
        for i in range(len(profs)):
            print(i)
            user_markup.row(profs[i][0])
        args.bot.send_message(parse_mode='HTML', chat_id=userID,
                              text='<i>Вы получили новый ранг, теперь вы можете выбрать новую профессию</i>',
                              reply_markup=user_markup)
        args.new_frof_list.append(userID)
    except Exception as e:
        print(e)


def start_job(userID, status, time):  # замена статуса и указание времени начала
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Status='{0}' WHERE ID='{1}'".format(str(status), str(userID)))
        cursor.execute("UPDATE Users SET End_time='{0}' WHERE ID='{1}'".format(str(time), str(userID)))
        connect.commit()
    except Exception as e:
        print(e)


def plus_count_works(userID):  # указание количества выполненных работ
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Count_Works=Count_Works+1 WHERE ID='{0}'".format(str(userID)))
        connect.commit()
        up_lvl(userID)  # повышение ранга
    except Exception as e:
        print(e)


def minus_money(userID, money):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Money=Money-{0} WHERE ID='{1}'".format(money, userID))
        connect.commit()
    except Exception as e:
        print(e)


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


def getReq(toID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT DISTINCT * FROM Requests WHERE toUserID={0}".format(toID))
    res = cursor.fetchall()
    print(res)
    print(len(res))
    msg = ''
    for i in range(len(res)):
        msg += str(res[i][1]) + ' /accept' + str(get_owner(res[i][1]))
        msg += '\n'
    return msg


def delete_request(userID):
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("DELETE FROM Requests WHERE toUserID={0}".format(userID))
    connect.commit()


def get_referal_owner(userID):
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
        print(e)
        return str('none')


def get_noInCorpUsers(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID,NickName,Profession FROM Users WHERE Comp='0' ORDER BY RANDOM() LIMIT 7")
        users = cursor.fetchall()
        msg_text = ''
        print('check')
        print(len(users[0]))
        print(len(users))
        for i in range(len(users)):
            if users[i][0] != message.from_user.id:
                print(i)
                msg_text += str(users[i][1]) + ' ' + str(users[i][2]) + ' /invite' + str(users[i][0])
                msg_text += '\n'
        return msg_text
    except Exception as e:
        print(e)


def UpdQuests():
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM {0}".format("Quests"))
    args.QuestsArr = []
    res = cursor.fetchall()
    for i in res:
        args.QuestsArr.append([i[0], i[1], i[2], i[3]])
    print("Список всех поступивших квестов: ")
    print(args.QuestsArr)


def UpdProf():  # Обновление полного списка профессий и профессий для начинающих
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Profs")
    args.ProfArr = cursor.fetchall()
    print("Список всех поступивших профессий: ")
    print(args.ProfArr)

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

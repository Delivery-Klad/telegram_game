"""
файл для работы с базой данных
"""
import sqlite3
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
                       'UserRank TEXT)')  # дата регистрации
        cursor.execute('CREATE TABLE IF NOT EXISTS Quests(Profession TEXT,'  # профессия 
                       'Quest TEXT,'  # задание
                       'Rank INTEGER,'  # ранг/сложность задания
                       'Time INTEGER)')  # время выполнения задания
        cursor.execute('CREATE TABLE IF NOT EXISTS Profs(Prof TEXT,'  # профессия 
                       'ProfCheck INTEGER,'
                       'ProfRank INTEGER)')  # 0/1/3 - гум/технарь/доступен всем
        connect.commit()
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


def start_job(userID, status, time):  # замена статуса и указание времени начала
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Status='{0}' WHERE ID='{1}'".format(str(status), str(userID)))
        cursor.execute("UPDATE Users SET End_time='{0}' WHERE ID='{1}'".format(str(time), str(userID)))
        connect.commit()
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


def plus_count_works(message):  # указание количества выполненных работ
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Count_Works=Count_Works+1 WHERE ID='{0}'".format(str(message.from_user.id)))
        connect.commit()
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


def set_nickname(nickName):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET NickName='{0}' WHERE ID='{1}'".format(str(nickName.text), str(nickName.from_user.id)))
        connect.commit()
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


def set_profession(message):
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
        elif message.text in args.gumList:
            cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(message.from_user.id))
            spec = cursor.fetchall()
            if spec[0][0] == 'gum':
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
        connect.commit()
        cursor.close()
        connect.close()
        return True
    except Exception as e:
        print(e)


def get_nickname(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT NickName FROM Users WHERE ID=" + str(userID))
        name = cursor.fetchall()
        connect.commit()
        cursor.close()
        connect.close()
        return name[0][0]
    except Exception as e:
        print(e)


def get_spec(userID):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Spec FROM Users WHERE ID=" + str(userID))
        spec = cursor.fetchall()
        connect.commit()
        cursor.close()
        connect.close()
        return spec[0][0]
    except Exception as e:
        print(e)


def upd_spec(userID, spec):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("UPDATE Users SET Spec='{0}' WHERE ID={1}".format(spec, str(userID)))
        connect.commit()
        cursor.close()
        connect.close()
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
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


def isFree(userID):  # проверить выполняет ли пользователь какую-либо работу
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT Status FROM Users WHERE ID=" + str(userID))
        status = cursor.fetchall()
        connect.commit()
        cursor.close()
        connect.close()
        if status[0][0] == args.waitStatus:
            return True
        else:
            return False
    except Exception as e:
        print(e)


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
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


def give_new_prof(userID):
    try:
        pass
        """
        
        отправлять список новых профессий, СНАЧАЛА ДОДЕЛАТЬ СПИСКИ
        
        """
    except Exception as e:
        print(e)


def get_workers(message):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        cursor.execute("SELECT ID,NickName,Profession FROM Users WHERE Status='{0}'".format(str(args.waitStatus)))
        users = cursor.fetchall()
        msg_text = ''
        for i in range(len(users[0])-1):
            if users[i][0] != message.from_user.id:
                print(i)
                msg_text += str(users[i][1]) + ' ' + str(users[i][2]) + ' /task' + str(users[i][0])
        connect.commit()
        cursor.close()
        connect.close()
        return msg_text
    except Exception as e:
        print(e)


def UpdQuests():
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM {}".format("Quests"))
    args.QuestsArr = []
    res = cursor.fetchall()
    for i in res:
        args.QuestsArr.append([i[0], i[1], i[2], i[3]])
    print(args.QuestsArr)
    connect.commit()
    cursor.close()
    connect.close()


def UpdProf():  #Оновление полного списка профессий и профессий для начинающих
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Profs")
    args.ProfArr = cursor.fetchall()
    print(args.ProfArr)
    connect.commit()
    cursor.close()
    connect.close()

    args.techList = []
    args.gumList = []
    LowProfRank = 0
    gumID = 0
    techID = 1

    for i in args.ProfArr:
        if(i[2] == LowProfRank and i[1] == techID):  #Заполнение techList профессиями
            args.techList.append(i[0])
        elif(i[2] == LowProfRank and i[1] == gumID):  #Заполнение gumList профессиями
            args.gumList.append(i[0])
        elif(i[2] == LowProfRank and i[1] == 3):
            args.lowList.append(i[0])

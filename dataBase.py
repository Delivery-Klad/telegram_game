"""
файл для работы с базой данных
"""
import sqlite3
import args

QuestsArr = []


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
                       'Start_time TEXT,'  # время начала выполнения задания
                       'Count_Works INTEGER,'  # количество выполненных заданий
                       'Reg_Date TEXT)')  # дата регистрации
        connect.commit()
        cursor.close()
        connect.close()
    except Exception as e:
        print(e)


def change_status(id, status, time):  # замена статуса и указание времени начала
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Status='{0}' WHERE ID='{1}'".format(str(status), str(id)))
    cursor.execute("UPDATE Users SET Start_time='{0}' WHERE ID='{1}'".format(str(time), str(id)))
    connect.commit()
    cursor.close()
    connect.close()


def plus_count_works(userId):  # указание количества выполненных работ
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("UPDATE Users SET Count_Works=Count_Works+1 WHERE ID='{0}'".format(str(userId)))
    connect.commit()
    cursor.close()
    connect.close()


def GetQuests():
    connect = sqlite3.connect(args.filesFolderName + args.databaseName)
    cursor = connect.cursor()
    cursor.execute("SELECT * FROM Quests")
    QuestsArr = []
    res = cursor.fetchall()
    for i in res:
        quet = [i[0], i[1], i[2], i[3]]
        print(quet)
        QuestsArr.append(quet)
    connect.close()
    return QuestsArr


class Quests():
    Profession = ""
    Quest = ""
    Rank = ""
    Time = ""

    def __init__(self, prof, quest, rank, time):
        self.Profession = prof
        self.Quest = quest
        self.Rank = rank
        self.Time = time
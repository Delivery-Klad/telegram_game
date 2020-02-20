"""
файл, выполняющий действия в зависимости от времени
"""
from datetime import datetime
import dataBase
import sqlite3
import functions
import args


def timer(bot):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        can = True
        while True:
            try:
                if int(datetime.now().strftime('%M')) % 2 == 0 and int(datetime.now().strftime('%S')) == 0:
                    if can:
                        cursor.execute("SELECT End_time FROM Users")
                        end_time = cursor.fetchall()
                        for i in range(len(end_time[0])):
                            if end_time[0][i] != 'None':
                                end_minutes = int(end_time[0][i])
                                mitutes_now = int(datetime.now().strftime('%M'))
                                if mitutes_now == end_minutes or mitutes_now > end_minutes:
                                    cursor.execute("SELECT ID FROM Users WHERE End_time=" + str(end_minutes))  # остановить выполнение работы
                                    userId = cursor.fetchall()
                                    for i in range(len(userId[0])):
                                        dataBase.plus_count_works(userId[i][0])  # +1 к выполненным заданиям
                                        dataBase.start_job(userId[i][0], args.waitStatus, 'None')  # статус ожидания работы и установка времени на None
                                        functions.end_work(userId[i][0])
                                        dataBase.up_lvl(userId[i][0])  # повышение ранга(если выпонено условие)
                        # bot.send_message(496537969, 'test')
                        # bot.send_message(441287694, 'test')
                        print('sending')
                    can = False  # чтобы не выполнялось несколько раз в секунду
                else:
                    can = True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

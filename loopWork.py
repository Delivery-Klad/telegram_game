"""
файл, выполняющий действия в зависимости от времени
"""
from datetime import datetime
import dataBase
import sqlite3
import functions
import args

"""

отдебажил функцию timer теперь выполнение, начисление очков и прочее работает корректно

"""


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
                        for i in range(len(end_time)):
                            if end_time[i][0] != 'None':
                                print(end_time[i][0])
                                end_minutes = int(end_time[i][0])
                                mitutes_now = int(datetime.now().strftime('%M'))
                                if mitutes_now == end_minutes or mitutes_now > end_minutes:
                                    cursor.execute("SELECT ID FROM Users WHERE End_time=" + str(end_minutes))  # остановить выполнение работы
                                    userId = cursor.fetchall()
                                    for u in range(len(userId[0])):
                                        print(userId[0][u])
                                        args.bot.send_message(parse_mode='HTML', chat_id=userId[0][u],
                                                              text='<b>Вы закончили выполнение задания</b>')
                                        dataBase.plus_count_works(userId[0][u])  # +1 к выполненным заданиям
                                        dataBase.start_job(userId[0][u], args.waitStatus, 'None')  # статус ожидания работы и установка времени на None
                        # bot.send_message(496537969, 'test')
                        # bot.send_message(441287694, 'test')
                        print('checking')
                        can = False  # чтобы не выполнялось несколько раз в секунду
                else:
                    can = True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

"""
файл, выполняющий действия в зависимости от времени
"""
from datetime import datetime
import dataBase
import sqlite3
import args

"""

отдебажил функцию timer теперь выполнение, начисление очков и прочее работает корректно

"""


def timer():
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
                                end_minutes = int(end_time[i][0])
                                mitutes_now = int(datetime.now().strftime('%M'))
                                if mitutes_now == end_minutes or mitutes_now > end_minutes:
                                    cursor.execute("SELECT ID FROM Users WHERE End_time=" + str(end_minutes))
                                    user_id = cursor.fetchall()
                                    for u in range(len(user_id[0])):
                                        money = dataBase.get_task_cost(user_id[0][u])
                                        args.bot.send_message(parse_mode='HTML', chat_id=user_id[0][u],
                                                              text='<b>Вы закончили выполнение задания</b>\nВаш '
                                                                   'заработок: ' + str(money) + args.currency)
                                        dataBase.plus_count_works(user_id[0][u])  # +1 к выполненным заданиям
                                        company = dataBase.get_corp(user_id[0][u])
                                        if company != '0':
                                            owner_id = dataBase.get_owner(company)
                                            dataBase.add_money(owner_id, int(money)/10)
                                        dataBase.add_money(user_id[0][u], money)
                                        dataBase.start_job(user_id[0][u], args.waitStatus, 'None')
                        print('------------\nchecking')
                        can = False  # чтобы не выполнялось несколько раз в секунду
                else:
                    can = True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

from datetime import datetime
import dataBase
import sqlite3
import args


def timer(bot):
    try:
        connect = sqlite3.connect(args.filesFolderName + args.databaseName)
        cursor = connect.cursor()
        can = True
        while True:
            try:
                if int(datetime.now().strftime('%M')) % 5 == 0 and int(datetime.now().strftime('%S')) == 0:
                    if can:
                        cursor.execute("SELECT Start_time FROM Users")
                        start_time = cursor.fetchall()
                        for i in range(len(start_time[0])):
                            if start_time[0][i] != 'None':
                                start_minutes = int(start_time[0][i])
                                mitutes_now = int(datetime.now().strftime('%M'))
                                if mitutes_now > 30 and mitutes_now - start_minutes > 30 or mitutes_now < 30 and start_minutes > 30:
                                    cursor.execute("SELECT ID FROM Users WHERE Start_time=" + str(start_minutes))  # остановить выполнение работы
                                    userId = cursor.fetchall()
                                    dataBase.plus_count_works(userId[0][0])
                                    dataBase.change_status(userId[0][0], args.waitStatus, 'None')
                        bot.send_message(496537969, 'test')
                        bot.send_message(441287694, 'test')
                        print('sending')
                    can = False
                else:
                    can = True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

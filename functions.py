"""
файл для всяких функций
"""
from datetime import datetime
import args


def log(message):  # запись лога сообщений
    try:
        file = open(args.filesFolderName + args.logFileName, 'a')
        file.write('\n' + args.delimiter_line + '\n')
        file.write(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        if message.from_user.username != 'None' and message.from_user.username is not None:
            file.write('\nСообщение от {0}, (id = {1})\nТекст - {2}'.format(message.from_user.username,
                                                                            str(message.from_user.id),
                                                                            message.text))
        else:
            file.write('\nСообщение от {0} {1}, (id = {2})\nТекст - {3}'.format(message.from_user.first_name,
                                                                                message.from_user.last_name,
                                                                                str(message.from_user.id),
                                                                                message.text))
        print('\n' + args.delimiter_line)
        print(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        print('Сообщение от {0}, (id = {1})\nТекст - {2}'.format(message.from_user.username,
                                                                 str(message.from_user.id),
                                                                 message.text))
        file.close()
    except Exception as e:
        print(e)


def notInLists(message):  # проверка есть ли пользователь в каком-либо списке
    try:
        return True
    except Exception as e:
        print(e)


def send_task(workerID, name, task):  # отправка задания пользователю
    try:
        args.bot.send_message(parse_mode='HTML', chat_id=workerID,
                              text='<i>Пользователь</i> <b>{0}</b> <i>отправил вам задание "{1}"\n/accept - '
                                   'Согласиться\n/cancel - Отказаться</i>'.
                              format(str(name), str(task)))
        return task
    except Exception as e:
        print(e)


def isAdmin(userID):  # проверка является ли пользователь админом
    try:
        if int(userID) in args.admins_list:
            return True
        else:
            return False
    except Exception as e:
        print(e)


def in_profArr(message):
    for i in range(len(args.ProfArr)):
        if message == args.ProfArr[i][0]:
            return True
    return False


def wrong_input(userID, spec):
    try:
        if spec == 'tech':
            args.bot.send_message(parse_mode='HTML', chat_id=userID,
                                  text='Ты вроде <b>умный</b> человек, но зачем ты отправляешь мне то, что я не должен '
                                       'обрабатывать?')
        elif spec == 'gym':
            args.bot.send_message(parse_mode='HTML', chat_id=userID,
                                  text='Ты вроде <b>не глупый</b>, но зачем ты отправляешь мне то, что я не должен '
                                       'обрабатывать?')
        else:
            args.bot.send_message(parse_mode='HTML', chat_id=userID,
                                  text='Я конечно понимаю, что у тебя <b>проблемы с головой</b>, но не надо мне '
                                       'отправлять то, что я не должен обрабатывать!')
        args.bot.send_sticker(userID, args.dyrka)
    except Exception as e:
        print(e)

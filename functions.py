"""
файл для всяких функций
"""
from datetime import datetime
import random
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


def send_task(name, task):  # отправка задания пользователю
    try:
        if task == 'Перенести':
            index = random.randint(0, len(args.props_arr) - 1)
            task += ' ' + args.props_arr[index]
        elif task.split()[0] == 'Перевести':
            index = random.randint(0, len(args.languages_arr) - 1)
            task += ' ' + args.languages_arr[index] + ' языка'
        elif task.split()[0] == 'Провести':
            index = random.randint(0, len(args.lessons_arr) - 1)
            task += ' ' + args.lessons_arr[index]
        elif task.split()[0] == 'Запустить':
            index = random.randint(0, len(args.stream_reason_arr) - 1)
            task += ' ' + args.stream_reason_arr[index]
        elif task.split()[0] == 'Доставить':
            index = random.randint(0, len(args.address_arr) - 1)
            task += ' ' + args.address_arr[index]
        msg = '<i>Пользователь</i> <b>' + str(name) + '</b> <i>отправил вам задание</i> "' + str(task) + '"'
        return msg
    except IndexError:
        msg = '<i>Пользователь</i> <b>' + str(name) + '</b> <i>отправил вам задание</i> "' + str(task) + '"'
        return msg


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

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


def isAdmin(ids):  # проверка является ли пользователь админом
    try:
        if int(ids) in args.admins_list:
            return True
        else:
            return False
    except Exception as e:
        print(e)

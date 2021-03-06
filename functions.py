"""
файл реализации функций бота
"""
from datetime import datetime
from PIL import Image
import random
import args


def error_log(reason):  # запись лога ошибок
    """
    :param reason: error reason
    :return: запись лога ошибок
    """
    try:
        file = open(args.filesFolderName + args.ErlogFileName, 'a')
        file.write('\n' + args.delimiter_line + '\n')
        file.write(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        print('\n' + args.delimiter_line)
        print(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        try:
            file.write(reason)
            print(reason)
            file.close()
        except Exception:
            pass
    except Exception as e:
        print(e)


def log(message):  # запись лога сообщений
    """
    :param message: message
    :return: запись лога сообщений
    """
    try:
        file = open(args.filesFolderName + args.logFileName, 'a')
        file.write('\n' + args.delimiter_line + '\n')
        file.write(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
        try:
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
        except AttributeError:
            if message.from_user.username != 'None' and message.from_user.username is not None:
                file.write('\nСообщение от {0}, (id = {1})\nТекст - {2}'.format(message.from_user.username,
                                                                                str(message.from_user.id),
                                                                                message.data))
            else:
                file.write('\nСообщение от {0} {1}, (id = {2})\nТекст - {3}'.format(message.from_user.first_name,
                                                                                    message.from_user.last_name,
                                                                                    str(message.from_user.id),
                                                                                    message.data))
            print('\n' + args.delimiter_line)
            print(str(datetime.now().strftime('%d-%m-%Y %H:%M:%S')))
            print('Сообщение от {0}, (id = {1})\nТекст - {2}'.format(message.from_user.username,
                                                                     str(message.from_user.id),
                                                                     message.data))
        file.close()
    except Exception as e:
        error_log(e)


def generate_avatar(head_id, body_id, face_id):
    """
    :param head_id: id of args.head_file_name
    :param body_id: id of args.body_file_name
    :param face_id: id of args.face_file_name
    :return: создание аватара для пользователя
    """
    try:
        # body = Image.open(args.avatar_directory + args.body_file_name[body_id-1])
        # head = Image.open(args.avatar_directory + args.head_file_name[head_id-1])
        # body.paste(head, (0, 0), head)
        # body.save(args.tempImageName)

        avatar = Image.open(args.avatar_directory + args.avatar_file_name[0])
        face = Image.open(args.avatar_directory + args.face_file_name[face_id])
        avatar.paste(face, (0, 0), face)
        avatar.save(args.tempImageName)
    except Exception as e:
        error_log(e)


def send_task(name, task):  # отправка задания пользователю
    """
    :param name: user's name
    :param task: task
    :return: отправка задания пользователю
    """
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


def is_admin(user_id):  # проверка является ли пользователь админом
    """
    :param user_id: user_id
    :return: является ли пользователь админом
    """
    try:
        if int(user_id) in args.admins_list:
            return True
        else:
            return False
    except Exception as e:
        error_log(e)


def in_prof_arr(message):  # что это такое? я хз прост)))0)))
    """
    :param message: message
    :return: xz
    """
    for i in range(len(args.ProfArr)):
        if message == args.ProfArr[i][0]:
            return True
    return False


def wrong_input(user_id, spec):  # функция обработки ошибочного ввода
    """
    :param user_id: user_id
    :param spec: user's spec
    :return: error
    """
    try:
        if spec == 'tech':
            args.bot.send_message(parse_mode='HTML', chat_id=user_id,
                                  text='Ты вроде <b>умный</b> человек, но зачем ты отправляешь мне то, что я не должен '
                                       'обрабатывать?')
        elif spec == 'gym':
            args.bot.send_message(parse_mode='HTML', chat_id=user_id,
                                  text='Ты вроде <b>не глупый</b>, но зачем ты отправляешь мне то, что я не должен '
                                       'обрабатывать?')
        else:
            args.bot.send_message(parse_mode='HTML', chat_id=user_id,
                                  text='Я конечно понимаю, что у тебя <b>проблемы с головой</b>, но не надо мне '
                                       'отправлять то, что я не должен обрабатывать!')
        args.bot.send_sticker(user_id, args.dyrka)
    except Exception as e:
        error_log(e)

from datetime import datetime


def timer(bot):
    try:
        can = True
        while True:
            try:
                if int(datetime.now().strftime('%M')) % 5 == 0 and int(datetime.now().strftime('%S')) == 0:
                    if can:
                        bot.send_message(496537969, 'test')
                        # bot.send_message(441287694, 'ti priemniy')
                        print('sending')
                    can = False
                else:
                    can = True
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
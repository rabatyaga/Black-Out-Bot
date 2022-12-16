from datetime import datetime
import telebot
from TOKEN import token, chatId
from notifiers import get_notifier
bot = telebot.TeleBot(token)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id, "Привіт!\nЦей бот створено для моніторингу графіка відключень світла у місті Львів. "
                                               "Також є можливість налаштувати сповіщення про відлючення світла відповідно до певної групи.\n"
                                               "Щоб продовжити натисніть /putin_huilo")
    elif message.text == '/putin_huilo':
        bot.send_message(message.from_user.id, 'Оберіть номер вашої групи:')


class Electricity:
    current_time = datetime.now().strftime("%H")

    TYPE_1 = {'1-5': 'Можливе Відключення',
              '5-9': 'Немає Енергії',
              '9-13': 'Є Енергія',
              '13-17': 'Можливе Відключення',
              '17-21': 'Немає Енергії',
              '21-1': 'Є Енергія'}

    TYPE_2 = {'1-5': 'Немає Енергії',
              '5-9': 'Є Світло',
              '9-13': 'Можливе Відкючення',
              '13-17': 'Немає Енергії',
              '17-21': 'Є Енергія',
              '21-1': 'Можливе Відключення'}

    TYPE_3 = {'1-5': 'Є Енергія',
              '5-9': 'Можливе Відключення',
              '9-13': 'Немає Енергії',
              '13-17': 'Є Енергія',
              '17-21': 'Можливе Відключення',
              '21-1': 'Немає Енергії'}

    GROUP_1 = {'Понеділок': TYPE_2,
               'Вівторок': TYPE_3,
               'Середа': TYPE_1,
               'Четвер': TYPE_2,
               "П'ятниця": TYPE_3,
               'Субота': TYPE_1,
               'Неділя': TYPE_2}

    GROUP_2 = {'Понеділок': TYPE_3,
               'Вівторок': TYPE_1,
               'Середа': TYPE_2,
               'Четвер': TYPE_3,
               "П'ятниця": TYPE_1,
               'Субота': TYPE_2,
               'Неділя': TYPE_3}

    GROUP_3 = {'Понеділок': TYPE_1,
               'Вівторок': TYPE_2,
               'Середа': TYPE_3,
               'Четвер': TYPE_1,
               "П'ятниця": TYPE_2,
               'Субота': TYPE_3,
               'Неділя': TYPE_1}

    def __init__(self, group, day, time=current_time):
        self.group = group
        self.day = day
        self.time = time

    def get_time_zone(self):
        return '-'.join(list(filter(lambda x: int(self.current_time) in range(int(x[0]), int(x[1])), map(lambda x: x.split('-'), self.TYPE_1.keys())))[0])

    def inform(self):
        pass
    def get_condition(self):
        if self.group == 1:
            return self.GROUP_1[self.day][self.get_time_zone()]
        elif self.group == 2:
            return self.GROUP_2[self.day][self.get_time_zone()]
        else:
            return self.GROUP_3[self.day][self.get_time_zone()]

    def get_day_sсhedule(self):
        if self.group == 1:
            return self.GROUP_1[self.day]
        elif self.group == 2:
            return self.GROUP_2[self.day]
        else:
            return self.GROUP_3[self.day]




bot.polling(none_stop=True, interval=0)


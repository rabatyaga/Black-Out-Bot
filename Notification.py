from datetime import datetime
import telebot
from TOKEN import token
from telebot import types
from Data import Dicts

bot = telebot.TeleBot(token)
class Electricity:
    current_time = datetime.now().strftime("%H")

    GROUP_1 = Dicts.GROUP_1
    GROUP_2 = Dicts.GROUP_2
    GROUP_3 = Dicts.GROUP_3

    def __init__(self, group, day=None, time=current_time):
        self.group = group
        self.day = day
        self.time = time

    def get_time_zone(self):
        if int(self.time) >= 21:
            return '21-1'
        else:
            return '-'.join(list(filter(lambda x: int(self.current_time) in range(int(x[0]), int(x[1])),
                                        map(lambda x: x.split('-'), Dicts.TYPE_1.keys())))[0])

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


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Привіт!\nЦей бот створено для моніторингу графіка відключень світла у місті Львів. "
                                    "Також є можливість налаштувати сповіщення про відлючення світла відповідно до певної групи.\n"
                                    "Щоб продовжити натисніть /putin_huilo")


@bot.message_handler(commands=['putin_huilo'])
def choose_group(message):
    markup_inline = types.InlineKeyboardMarkup()
    group_1 = types.InlineKeyboardButton(text='Перша група', callback_data=1)
    group_2 = types.InlineKeyboardButton(text='Друга група', callback_data=2)
    group_3 = types.InlineKeyboardButton(text='Третя група', callback_data=3)
    markup_inline.add(group_1, group_2, group_3)
    bot.send_message(message.chat.id, 'Оберіть номер вашої групи:', reply_markup=markup_inline)

@bot.callback_query_handler(func= lambda call: True)
def choose_day(call):
    if call.data in ('1', '2', '3'):
        new = Electricity(call.data)
        markup_inline_2 = types.InlineKeyboardMarkup()
        monday = types.InlineKeyboardButton(text='Понеділок', callback_data='Понеділок')
        tuesday = types.InlineKeyboardButton(text='Вівторок', callback_data='Вівторок')
        wednesday = types.InlineKeyboardButton(text='Середа', callback_data='Середа')
        thursday = types.InlineKeyboardButton(text='Четвер', callback_data='Четвер')
        friday = types.InlineKeyboardButton(text="П'ятниця", callback_data="П'ятниця")
        saturday = types.InlineKeyboardButton(text="Субота", callback_data="Субота")
        sunday = types.InlineKeyboardButton(text="Неділя", callback_data="Неділя")
        markup_inline_2.add(monday, tuesday, wednesday, thursday, friday, saturday, sunday)
        bot.send_message(call.message.chat.id, 'Оберіть день:', reply_markup=markup_inline_2)

@bot.callback_query_handler(func= lambda call: True)
def print_schedule(call):
    print(call)
    bot.send_message(call.message.chat.id, str(Electricity(call).get_day_sсhedule()))





bot.polling(none_stop=True, interval=0)

a = Electricity(1, 'Понеділок')
print(a.get_condition())


import json
from datetime import datetime
import telebot
from TOKEN import token
from telebot import types
from Data import Dicts

bot = telebot.TeleBot(token)
class Electricity:
    current_time = datetime.now().strftime("%H")
    current_day = datetime.today().weekday()

    GROUP_1 = Dicts.GROUP_1
    GROUP_2 = Dicts.GROUP_2
    GROUP_3 = Dicts.GROUP_3

    def __init__(self, group, time=current_time):
        self.group = group
        self.time = time

    def get_time_zone(self):
        if int(self.time) >= 21:
            return '21-1'
        else:
            ranges = map(lambda x: x.split('-'), Dicts.TYPE_1.keys())
            return '-'.join(list(filter(lambda x: int(self.current_time) in range(int(x[0]), int(x[1])), ranges))[0])

    def inform(self):
        pass

    def callback_inf(self, callback, l=[]):
        self.l = l
        self.callback = callback
        self.l.append(self.callback)
        return self.l

    def get_condition(self, day=current_day):
        self.day = day
        if self.group == 1:
            return self.GROUP_1[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]
        elif self.group == 2:
            return self.GROUP_2[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]
        else:
            return self.GROUP_3[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]

    def get_day_sсhedule(self, day):
        self.day = day
        if self.group == 1:
            return self.GROUP_1[self.day]
        elif self.group == 2:
            return self.GROUP_2[self.day]
        else:
            return self.GROUP_3[self.day]




@bot.message_handler(commands=['start'])
def start_message(message):
    img = open(Dicts.PICTURE_1, 'rb')
    bot.send_photo(message.chat.id, img, caption="<b>Привіт!\nЦей бот створено для моніторингу графіка відключень світла у місті Львів. "
                                    "Також є можливість налаштувати сповіщення про відключення світла відповідно до певної групи.\n"
                                    "Щоб продовжити натисніть /putin_huilo</b>", parse_mode='HTML')



@bot.message_handler(commands=['putin_huilo'])
def choose_option(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton(text='Отримати поточний стан згідно графіку')
    btn2 = types.KeyboardButton(text='Отримати графік відключення на обраний день')
    btn3 = types.KeyboardButton(text='Налаштувати сповіщення щодо відключення')
    kb.add(btn1, btn2, btn3)
    msg = bot.send_message(message.chat.id, text='<b>Оберіть опцію:</b>', reply_markup=kb, parse_mode='HTML')
    bot.register_next_step_handler(msg, option)


def option(message):
    if message.text == 'Отримати поточний стан згідно графіку':
        choose_group(message)
        # bot.send_message(message.chat.id, Electricity(resp).get_condition())

@bot.message_handler(content_types=['text'])
def choose_group(message):
    bot.send_message(message.chat.id, f'Ви обрали опцію:\n{message.text}')
    markup_inline = types.InlineKeyboardMarkup()
    group_1 = types.InlineKeyboardButton(text='I група', callback_data=1)
    group_2 = types.InlineKeyboardButton(text='II група', callback_data=2)
    group_3 = types.InlineKeyboardButton(text='III група', callback_data=3)
    markup_inline.add(group_1, group_2, group_3)
    bot.send_message(message.chat.id, 'Оберіть номер вашої групи:', reply_markup=markup_inline)

@bot.callback_query_handler(func= lambda callback: callback.data)
def to_json(callback):
    with open('user_data.json', 'r') as f_o:
        data_from_json = json.load(f_o)
    user_id = callback.from_user.id
    group_id = callback.data
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {'group': group_id}
    else:
        del data_from_json[str(user_id)]
        data_from_json[user_id] = {'group': group_id}
    with open('user_data.json', 'w') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    bot.send_message(callback.message.chat.id, text=f'Ви зареєстровані: {user_id}\n'
                                                    f'Ваша група: {group_id}')
    with open('user_data.json', 'r') as f_o:
        data_from_json = json.load(f_o)
        bot.send_message(callback.message.chat.id, text=Electricity(int(data_from_json[str(user_id)]['group'])).get_condition())


# @bot.callback_query_handler(func= lambda x: True)
# def choose_day(callback):
#      markup_inline_2 = types.InlineKeyboardMarkup()
#      monday = types.InlineKeyboardButton(text='Понеділок', callback_data='Понеділок')
#      tuesday = types.InlineKeyboardButton(text='Вівторок', callback_data='Вівторок')
#      wednesday = types.InlineKeyboardButton(text='Середа', callback_data='Середа')
#      thursday = types.InlineKeyboardButton(text='Четвер', callback_data='Четвер')
#      friday = types.InlineKeyboardButton(text="П'ятниця", callback_data="П'ятниця")
#      saturday = types.InlineKeyboardButton(text="Субота", callback_data="Субота")
#      sunday = types.InlineKeyboardButton(text="Неділя", callback_data="Неділя")
#      markup_inline_2.add(monday, tuesday, wednesday, thursday, friday, saturday, sunday)
#      bot.send_message(callback.message.chat.id, text='Оберіть день:', reply_markup=markup_inline_2)








bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling()



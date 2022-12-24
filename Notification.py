import json
from datetime import datetime
import telebot
from telebot import types
from Data import Dicts
import requests
from envparse import Env
from telegram_client import TelegramClient

"""Створення змінних оточення"""
env = Env()
TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = env.int("ADMIN_CHAT_ID")


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.telegram_client = telegram_client



telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
bot = MyBot(token=TOKEN, telegram_client=telegram_client)


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

    def get_condition(self, day=current_day):
        self.day = day
        if self.group == 1:
            return self.GROUP_1[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]
        elif self.group == 2:
            return self.GROUP_2[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]
        else:
            return self.GROUP_3[Dicts.WEEK_DAY[self.day]][self.get_time_zone()]

    def get_day_sсhedule(self, day=current_day):
        self.day = day
        if self.group == 1:
            return self.GROUP_1[Dicts.WEEK_DAY[self.day]]
        elif self.group == 2:
            return self.GROUP_2[Dicts.WEEK_DAY[self.day]]
        else:
            return self.GROUP_3[Dicts.WEEK_DAY[self.day]]






@bot.message_handler(commands=['start'])
def start_message(message):
    img = open(Dicts.PICTURE_1, 'rb')
    bot.send_photo(message.chat.id, img, caption="Привіт!\nЦей бот створено для моніторингу графіка відключень світла"
                                                 " у місті Львів. "
                                    "Також є можливість налаштувати сповіщення про відключення світла відповідно до "
                                                 "певної групи.\n"
                                    "Щоб продовжити натисніть <b>/putin_huilo</b>", parse_mode='HTML')




@bot.message_handler(commands=['putin_huilo'])
def choose_group(message):
    markup_inline = types.InlineKeyboardMarkup()
    group_1 = types.InlineKeyboardButton(text='I група', callback_data=1)
    group_2 = types.InlineKeyboardButton(text='II група', callback_data=2)
    group_3 = types.InlineKeyboardButton(text='III група', callback_data=3)
    markup_inline.add(group_1, group_2, group_3)
    bot.send_message(message.chat.id, '<b>Оберіть номер вашої групи:</b>', reply_markup=markup_inline, parse_mode='HTML')
    markup_inline_2 = types.InlineKeyboardMarkup()
    url = types.InlineKeyboardButton(text='Дізнатись групу', url='https://poweroff.loe.lviv.ua/gav_city3')
    markup_inline_2.add(url)
    bot.send_message(message.chat.id, '<b>Не знаєте в якій ви групі?</b>', reply_markup=markup_inline_2,
                     parse_mode='HTML')


@bot.callback_query_handler(func=lambda callback: callback.data)
def to_json(callback):
    with open('user_data.json', 'r', encoding='utf-8') as f_o:
        data_from_json = json.load(f_o)
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    group_id = callback.data
    if str(user_id) not in data_from_json:
        data_from_json[user_id] = {'group': group_id, 'username': user_name}
    else:
        del data_from_json[str(user_id)]
        data_from_json[user_id] = {'group': group_id}
    with open('user_data.json', 'w', encoding='utf-8') as f_o:
        json.dump(data_from_json, f_o, indent=4, ensure_ascii=False)
    bot.send_message(callback.message.chat.id, text=f'Вітаю, {user_name}. Вас зареєстровано.\n'
                                                    f'Ваша група: №{group_id}')
    choose_option(callback.message)


def choose_option(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    btn1 = types.KeyboardButton(text='1 💡')
    btn2 = types.KeyboardButton(text='2 🕯')
    btn3 = types.KeyboardButton(text='3 📅')
    btn4 = types.KeyboardButton(text='4 ⏰')
    btn5 = types.KeyboardButton(text='5 🔁')
    kb.add(btn1, btn2, btn3, btn4, btn5)
    msg = bot.send_message(message.chat.id, text='<b>Оберіть опцію:</b>', reply_markup=kb, parse_mode='HTML')

    bot.send_message(message.chat.id, text='1. Дізнатись про наявність електроенергії у цю мить.\n'
                                           '2. Отримати графік відключення на поточний день.\n'
                                           '3. Отримати графік відключення на тиждень.\n'
                                           '4. Налаштувати сповіщення щодо відключення.\n'
                                           '5. Змінити групу.')
    bot.register_next_step_handler(msg, option)


def option(message):
    with open('user_data.json', 'r', encoding='utf-8') as f_o:
        data_from_json = json.load(f_o)
        group = data_from_json[str(message.chat.id)]['group']
    if message.text == '1 💡':
        condition = Electricity(int(group)).get_condition()
        if condition == 'Є Енергія':
            img = open(Dicts.PICTURE_2, 'rb')
            bot.send_photo(message.chat.id, img, caption=f'Згідно графіку відключень від Львівобленерго у вашому будинку'
                                                         f' на цей момент імовірно:\n'
                                                         f'<b>✅ {condition} ✅</b>',
                           parse_mode='HTML')
        elif condition == 'Немає Енергії':
            img = open(Dicts.PICTURE_3, 'rb')
            bot.send_photo(message.chat.id, img, caption=f'Згідно графіку відключень від Львівобленерго у вашому будинку'
                                                         f' на цей момент імовірно:\n'
                                                         f'<b>❌ {condition} ❌</b>',
                           parse_mode='HTML')
        else:
            img = open(Dicts.PICTURE_4, 'rb')
            bot.send_photo(message.chat.id, img,
                           caption=f'Згідно графіку відключень від Львівобленерго у вашому будинку'
                                   f' на цей момент імовірно:\n'
                                   f'<b>⚠️ {condition} ⚠️</b>',
                           parse_mode='HTML')
        choose_option(message)
    elif message.text == '2 🕯':
        bot.send_message(message.chat.id, text=f'<b>{Dicts.WEEK_DAY[Electricity.current_day]}, Група №{group}</b>',
                         parse_mode='HTML')
        condition = Electricity(int(group)).get_day_sсhedule()
        for k, v in condition.items():
            bot.send_message(message.chat.id, text=f'<b>{k} : {v}</b>', parse_mode='HTML')
        choose_option(message)
    elif message.text == '3 📅':
        if group == '1':
            img = open(Dicts.SCHEDULE_1, 'rb')
            bot.send_photo(message.chat.id, img)
        elif group == '2':
            img = open(Dicts.SCHEDULE_2, 'rb')
            bot.send_photo(message.chat.id, img)
        else:
            img = open(Dicts.SCHEDULE_3, 'rb')
            bot.send_photo(message.chat.id, img)
        choose_option(message)
    # elif message.text == '4 ⏰':
    #     while True:
    #         time.sleep(60)
    #         if Electricity.current_time == '12:00':  # Выставляете ваше время
    #             print('pass')
    #             bot.send_message("тут айди вашей группы", 'text')

    elif message.text == '5 🔁':
        choose_group(message)




def create_err_message(err: Exception) -> str:
    return f"{datetime.now} ::: {err.__class__} ::: {err}"



while True:
    try:
        bot.polling()
    except Exception as err:
        bot.telegram_client.post(method='sendMessage', params={"text": create_err_message(err),
                                                               "chat_id": ADMIN_CHAT_ID})




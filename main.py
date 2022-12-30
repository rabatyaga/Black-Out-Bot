from datetime import datetime
import telebot
from telebot import types
from Data import Dicts
from envparse import Env
from telegram_client import TelegramClient
from sqlclient import SQLiteClient, UserActioner
from logging import getLogger, StreamHandler

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")

"""Створення змінних оточення"""
env = Env()
TOKEN = env.str("TOKEN")
ADMIN_CHAT_ID = env.int("ADMIN_CHAT_ID")


class MyBot(telebot.TeleBot):
    def __init__(self, telegram_client: TelegramClient, user_actioner: UserActioner, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.telegram_client = telegram_client
        self.user_actioner = user_actioner

    def setup_resources(self):
        self.user_actioner.setup()

    def shutdown_resources(self):
        self.user_actioner.shutdown()

    def shutdown(self):
        self.shutdown_resources()


user_actioner = UserActioner(SQLiteClient('users.db'))
telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
bot = MyBot(token=TOKEN, telegram_client=telegram_client, user_actioner=user_actioner)


class Electricity:
    current_time = datetime.now().strftime("%H")
    current_day = datetime.today().weekday()

    GROUP_1 = Dicts.GROUP_1
    GROUP_2 = Dicts.GROUP_2
    GROUP_3 = Dicts.GROUP_3

    def choose_day(self):
        if self.current_time == '00':
            if self.current_day != 1:
                return self.current_day - 1
            else:
                return 6
        else:
            return self.current_day

    def get_time_zone(self):
        if int(self.current_time) >= 21 or int(self.current_time) == 0:
            return '21-1'
        else:
            ranges = map(lambda x: x.split('-'), Dicts.TYPE_1.keys())
            return '-'.join(list(filter(lambda x: int(self.current_time) in range(int(x[0]), int(x[1])), ranges))[0])

    def inform(self, current_condition: str):
        right_border = self.get_time_zone().split('-')[1]
        difference = int(right_border) - int(self.current_time)
        if current_condition in ("Можливе Відключення", "Є Енергія") and difference == 1:
            return True
        else:
            return False



    def get_condition(self, group: int) -> str:
        day = self.choose_day()
        if group == 1:
            return self.GROUP_1[Dicts.WEEK_DAY[day]][self.get_time_zone()]
        elif group == 2:
            return self.GROUP_2[Dicts.WEEK_DAY[day]][self.get_time_zone()]
        else:
            return self.GROUP_3[Dicts.WEEK_DAY[day]][self.get_time_zone()]

    def get_day_sсhedule(self, group: int) -> dict:
        day = self.choose_day()
        if group == 1:
            return self.GROUP_1[Dicts.WEEK_DAY[day]]
        elif group == 2:
            return self.GROUP_2[Dicts.WEEK_DAY[day]]
        else:
            return self.GROUP_3[Dicts.WEEK_DAY[day]]





@bot.message_handler(commands=['start'])
def start_message(message):
    img = open(Dicts.PICTURE_1, 'rb')
    bot.send_photo(message.chat.id, img, caption="Привіт!\nЦей бот послуговується графіками <b>планових</b> відключень від "
                                                 "Львівобленерго. Інформація про <b>аварійні</b> відключення не надається. "
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
    tg_name = callback.from_user.username
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    chat_id = callback.message.chat.id
    group_id = callback.data

    user = bot.user_actioner.get_user(user_id=str(user_id))

    if not user:
        bot.user_actioner.create_user(user_id=str(user_id), username=user_name, chat_id=chat_id, tg_name=tg_name)
        bot.user_actioner.set_group(user_id=str(user_id), group_id=group_id)
    else:
        bot.user_actioner.set_group(user_id=str(user_id), group_id=group_id)


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
    group = bot.user_actioner.get_group(user_id=str(message.from_user.id))
    if message.text == '1 💡':
        condition = Electricity().get_condition(int(group))
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
        bot.send_message(message.chat.id, text=f'<b>{Dicts.WEEK_DAY[Electricity().choose_day()]}, Група №{group}</b>',
                         parse_mode='HTML')
        condition = Electricity().get_day_sсhedule(int(group))
        for k, v in condition.items():
            bot.send_message(message.chat.id, text=f'<b>{k} : {v}</b>', parse_mode='HTML')
        choose_option(message)
    elif message.text == '3 📅':
        if group == 1:
            img = open(Dicts.SCHEDULE_1, 'rb')
            bot.send_photo(message.chat.id, img)
        elif group == 2:
            img = open(Dicts.SCHEDULE_2, 'rb')
            bot.send_photo(message.chat.id, img)
        else:
            img = open(Dicts.SCHEDULE_3, 'rb')
            bot.send_photo(message.chat.id, img)
        choose_option(message)
    elif message.text == '4 ⏰':
        bot.send_message(message.chat.id, text=f'Вітаю, {user_actioner.get_user(user_id=str(message.from_user.id))[1]}. '
                                               f'Ви підключили сповіщення!\n'
                                               'Кожного разу за годину перед можливим відключенням '
                                               'Вам надходитиме попереджувальне повідомлення.')

        bot.user_actioner.set_notify(user_id=str(message.from_user.id), notifications=1)
        choose_option(message)
    elif message.text == '5 🔁':
        choose_group(message)




def create_err_message(err: Exception) -> str:
    return f"{datetime.now} ::: {err.__class__} ::: {err}"



if __name__ == "__main__":
    while True:
        try:
            bot.setup_resources()
            bot.polling()
        except Exception as err:
            error_message = create_err_message(err)
            bot.telegram_client.post(method='sendMessage', params={"text": error_message,
                                                                   "chat_id": ADMIN_CHAT_ID})

            logger.error(error_message)
            bot.shutdown()




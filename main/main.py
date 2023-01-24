from datetime import datetime
import telebot
from telebot import types
from resources.Data import Dicts
from resources.electricity import *
from resources.TOKEN import token, chatId
from clients.telegram_client import TelegramClient
from clients.sqlclient import SQLiteClient, UserActioner
# from logger_main import *

TOKEN = token
ADMIN_CHAT_ID = chatId


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


user_actioner = UserActioner(SQLiteClient(r"../resources/users.db"))
telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
bot = MyBot(token=TOKEN, telegram_client=telegram_client, user_actioner=user_actioner)



@bot.message_handler(commands=['start'])
def start_message(message):
    img = open(Dicts.PICTURE_1, 'rb')
    msg = bot.send_photo(message.chat.id, img, caption="Привіт!\nЦей бот послуговується графіками <b>планових</b> відключень від "
                                                 "Львівобленерго. Інформація про <b>аварійні</b> відключення не надається. "
                                    "Щоб продовжити натисніть <b>/putin_huilo</b>", parse_mode='HTML')
    bot.register_next_step_handler(msg, reply_to_start)



def reply_to_start(message):
    if message.text != "/putin_huilo":
        bot.reply_to(message, "Для початку роботи із ботом необхідно ідентифікувати ваші політичні погляди, тому щоб продовжити, "
                          "слідуйте інструкціям, що вказані нижче 👇🏻", parse_mode='HTML')
        start_message(message)
    else:
        choose_group(message)


# @bot.message_handler(commands=['putin_huilo'])
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



@bot.message_handler(content_types=["text"])
def reply(message):
    bot.reply_to(message, "Спершу <b>оберіть групу! ☝🏻</b>\nДля взаємодії з ботом використовуйте клавіші, що з'являються у чаті та "
                          "у нижній частині екрану.", parse_mode='HTML')



@bot.callback_query_handler(func=lambda callback: callback.data)
def to_json(callback):

    tg_name = callback.from_user.username
    user_id = callback.from_user.id
    user_name = callback.from_user.first_name
    chat_id = callback.message.chat.id
    group_id = callback.data
    bot.delete_message(callback.message.chat.id, callback.message.id)

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

def on_off(message):
    if message.text == "Підключити сповіщення":
        bot.send_message(message.chat.id, text=f'Вітаю, {user_actioner.get_user(user_id=str(message.from_user.id))[1]}. '
                                               f'Ви підключили сповіщення!\n'
                                               'Кожного разу за годину перед можливим відключенням '
                                               'Вам надходитиме попереджувальне повідомлення.')

        bot.user_actioner.set_notify(user_id=str(message.from_user.id), notifications=1)
        choose_option(message)
    elif message.text == "Відключити сповіщення":
        bot.send_message(message.chat.id,
                         text="Сповіщення про відключення електроенергії вимкнено !")
        bot.user_actioner.set_notify(user_id=str(message.from_user.id), notifications=0)
        choose_option(message)
    else:
        bot.reply_to(message, text="Для взаємодії з ботом використовуйте клавіші, що з'являються у "
                          "нижній частині екрану. Спробуйте підключити або відключити сповіщення ще раз, "
                                   "використовуючи одну із запропонованих опцій.")
        choose_option(message)



def option(message):
    group = bot.user_actioner.get_group(user_id=str(message.from_user.id))
    if message.text == '1 💡':
        condition = get_condition(int(group))
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
        bot.send_message(message.chat.id, text=f'<b>{Dicts.WEEK_DAY[choose_day()]}, Група №{group}</b>',
                         parse_mode='HTML')
        condition = get_day_sсhedule(int(group))
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
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton(text='Підключити сповіщення')
        btn2 = types.KeyboardButton(text='Відключити сповіщення')
        kb.add(btn1, btn2)
        msg = bot.send_message(message.chat.id, text='<b>Оберіть опцію:</b>', reply_markup=kb, parse_mode='HTML')
        bot.register_next_step_handler(msg, on_off)

    elif message.text == '5 🔁':
        choose_group(message)

    else:
        bot.reply_to(message, text="Для взаємодії з ботом використовуйте <b>клавіатуру у нижній частині екрану!</b> "
                                               "Вдалого користування.", parse_mode='HTML')
        choose_option(message)




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

            send_log(error_message)
            bot.shutdown()




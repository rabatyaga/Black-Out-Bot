from clients.sqlclient import SQLiteClient
from clients.telegram_client import TelegramClient
from resources.TOKEN import token
from reminder import Reminder
from datetime import datetime
import time

from logger_reminder import *


TOKEN = token


database_client = SQLiteClient(r"../resources/users.db")
telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
reminder = Reminder(database_client=database_client, telegram_client=telegram_client)
reminder.setup()




while True:
    now = datetime.now()
    if now.minute == 1:
        send_log('Started notification' + '=' * 100)
        reminder()
        send_log('Ended notification ' + '=' * 100)
        time.sleep(60)
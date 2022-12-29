from sqlclient import SQLiteClient
from telegram_client import TelegramClient
from logging import getLogger, StreamHandler
from envparse import Env
from main import Electricity
from reminder import Reminder
from datetime import datetime

import time
logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
env = Env()
TOKEN = env.str("TOKEN")


database_client = SQLiteClient("users.db")
telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
electricity = Electricity()
reminder = Reminder(database_client=database_client, telegram_client=telegram_client, electricity=electricity)
reminder.setup()

while True:
    current_time = datetime.now().strftime("%H.%M")
    if current_time.split('.')[1] == '00':
        reminder()
        time.sleep(60)

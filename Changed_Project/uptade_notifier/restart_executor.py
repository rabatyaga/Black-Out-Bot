from clients.sqlclient import SQLiteClient
from clients.telegram_client import TelegramClient
from resources.TOKEN import token
from restart import Restart



TOKEN = token


database_client = SQLiteClient(r"../resources/users.db")
telegram_client = TelegramClient(token=TOKEN, base_url="https://api.telegram.org")
restart = Restart(database_client=database_client, telegram_client=telegram_client)
restart.setup()
restart()



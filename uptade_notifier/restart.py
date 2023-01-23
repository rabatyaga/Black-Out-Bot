from clients.sqlclient import SQLiteClient
from clients.telegram_client import TelegramClient
from resources.TOKEN import token


TOKEN = token

class Restart:
    GET_NOTIFY = """
        SELECT chat_id FROM users;
        """

    def __init__(self, telegram_client: TelegramClient, database_client: SQLiteClient):
        self.telegram_client = telegram_client
        self.database_client = database_client
        self.setted_up = False

    def setup(self):
        self.database_client.create_conn()
        self.setted_up = True

    def shutdown(self):
        self.database_client.close_conn()

    def notify(self, chat_ids: list):
        for chat_id in chat_ids:
            self.telegram_client.post(method="sendMessage",
                                      params={
                                          "text": "У боті була проведена модифікація та виправлення помилок. "
                                                  "Щоб продовжити користування ботом натисніть /start",
                                          "chat_id": chat_id})

    def execute(self):
        chat_ids = self.database_client.execute_select_command(self.GET_NOTIFY)
        if chat_ids:
            self.notify(chat_ids=chat_ids)

    def __call__(self, *args, **kwargs):
        if not self.setted_up:
            return
        self.execute()



from clients.sqlclient import SQLiteClient
from clients.telegram_client import TelegramClient
from resources.TOKEN import token
from electricity import *
from resources.Data import Dicts

from logger_reminder import *

TOKEN = token

class Reminder:
    GET_NOTIFY = """
        SELECT chat_id, group_id FROM users WHERE notifications is 1;
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
            next_con = get_next_condition(chat_id[1])
            send_log(f"Inform status for chat_id {chat_id}: {inform(chat_id[1])}")
            res = ''
            if inform(chat_id[1]) == True:
                if next_con == "Можливе Відключення":
                    res = self.telegram_client.post(method="sendMessage",
                                                    params={
                                                        "text": "⚠️ Увага ! За годину можливе відключення електроенергії ! ⚠️",
                                                        "chat_id": chat_id[0]})
                elif next_con == "Немає Енергії":
                    res = self.telegram_client.post(method="sendMessage",
                                                    params={
                                                        "text": "❗️ Увага ! За годину планове відключення електроенергії ! ❗️",
                                                        "chat_id": chat_id[0]})


            send_log(f'Next condition: {next_con}, got result: {res}')

    def execute(self):
        chat_ids = self.database_client.execute_select_command(self.GET_NOTIFY)
        if chat_ids:
            self.notify(chat_ids=chat_ids)

    def __call__(self, *args, **kwargs):
        if not self.setted_up:
            logger.error("Resources has not been setted up!")
            return
        self.execute()



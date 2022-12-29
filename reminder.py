from sqlclient import SQLiteClient
from telegram_client import TelegramClient
from logging import getLogger, StreamHandler
from envparse import Env
from main import Electricity

logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")
env = Env()
TOKEN = env.str("TOKEN")

class Reminder:
    GET_NOTIFY = """
        SELECT chat_id, group_id FROM users WHERE notifications is 1;
        """

    def __init__(self, telegram_client: TelegramClient, database_client: SQLiteClient, electricity: Electricity):
        self.telegram_client = telegram_client
        self.database_client = database_client
        self.electricity = electricity
        self.setted_up = False

    def setup(self):
        self.database_client.create_conn()
        self.setted_up = True

    def shutdown(self):
        self.database_client.close_conn()

    def notify(self, chat_ids: list):
        for chat_id in chat_ids:
            con = self.electricity.get_condition(chat_id[1])
            if self.electricity.inform(con) == True:
                if con == "Є Енергія":
                    res = self.telegram_client.post(method="sendMessage",
                                                    params={
                                                        "text": "⚠️ Увага ! За годину можливе відключення електроенергії ! ⚠️",
                                                        "chat_id": chat_id[0]})
                elif con == "Можливе Відключення":
                    res = self.telegram_client.post(method="sendMessage",
                                                    params={
                                                        "text": "❗️ Увага ! За годину планове відключення електроенергії ! ❗️",
                                                        "chat_id": chat_id[0]})


                logger.info(res)

    def execute(self):
        chat_ids = self.database_client.execute_select_command(self.GET_NOTIFY)
        if chat_ids:
            self.notify(chat_ids=chat_ids)

    def __call__(self, *args, **kwargs):
        if not self.setted_up:
            logger.error("Resources has not been setted up!")
            return
        self.execute()


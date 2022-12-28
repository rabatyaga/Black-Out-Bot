import sqlite3

class SQLiteClient:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.conn = None

    def create_conn(self):
        self.conn = sqlite3.connect(self.filepath, check_same_thread=False)

    def close_conn(self):
        self.conn.close()

    def execute_command(self, command: str, params: tuple):
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError("you need to create connection to database!")

    def execute_select_command(self, command: str):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        else:
            raise ConnectionError("you need to create connection to database!")


class UserActioner:

    CREATE_USER = """
    INSERT INTO users (user_id, username, chat_id, tg_name) VALUES (?, ?, ?, ?);
    """

    GET_USER = """
    SELECT user_id, username, chat_id FROM users WHERE user_id = %s;
    """

    SET_GROUP = """
    UPDATE users SET group_id = ? WHERE user_id = ?;
    """

    GET_GROUP = """
    SELECT group_id FROM users WHERE user_id = %s;
    """

    SET_NOTIFY = """
    UPDATE users SET notifications = ? WHERE user_id = ?;
    """

    GET_NOTIFY = """
    SELECT chat_id, group_id FROM users WHERE notifications IS 1;
    """

    def __init__(self, database_client: SQLiteClient):
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()

    def shutdown(self):
        self.database_client.close_conn()

    def create_user(self, user_id: str, username: str, chat_id: int, tg_name: str):
        self.database_client.execute_command(self.CREATE_USER, (user_id, username, chat_id, tg_name))

    def get_user(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_USER % user_id)
        return user[0] if user else []

    def set_group(self, user_id: str, group_id: int):
        self.database_client.execute_command(self.SET_GROUP, (group_id, user_id))

    def get_group(self, user_id: str):
        user = self.database_client.execute_select_command(self.GET_GROUP % user_id)
        return user[0][0]

    def set_notify(self, user_id: str, notifications: int):
        self.database_client.execute_command(self.SET_NOTIFY, (notifications, user_id))

    def get_notify(self):
        users = self.database_client.execute_select_command(self.GET_NOTIFY)
        return users


# sql_client = UserActioner(SQLiteClient('users.db'))
# sql_client.setup()
# print(sql_client.get_notify())
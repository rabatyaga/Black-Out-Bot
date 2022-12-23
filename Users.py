import sqlite3

class SQLiteClient:

    def __init__(self, filepath: str):
        self.filepath = filepath
        self.conn = None

    def create_conn(self):
        self.conn = sqlite3.connect(self.filepath, check_same_thread=False)

    def execute_command(self, command: str):
        if self.conn is not None:
            self.conn.execute(command)
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

    def __init__(self, database_client: SQLiteClient):
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()

    def get_user(self, user_id: str):
        GET_USER = f"SELECT user_id, username, chat_id FROM users WHERE user_id = {user_id};"
        user = self.database_client.execute_select_command(GET_USER)
        return user[0] if user else []

    def create_user(self, user_id: str, username: str, chat_id: int):
        CREATE_USER = f"INSERT INTO users (user_id, username, chat_id) VALUES ({user_id}, '{username}', {chat_id});"
        self.database_client.execute_command(CREATE_USER)

    def set_group(self, user_id: str, group_id: int):
        SET_GROUP = f"UPDATE users SET group_id = {group_id} WHERE user_id = {user_id};"
        self.database_client.execute_command(SET_GROUP)


# import sqlite3
# conn = sqlite3.connect('users.db')
# cursor = conn.cursor()
#
# CREATE_QUERY = """
#     CREATE TABLE IF NOT EXISTS users (
#         user_id int PRIMARY KEY,
#         username text,
#         chat_id int,
#         group_id int
#     );
# """
# conn.execute(CREATE_QUERY)
#
# conn.commit()
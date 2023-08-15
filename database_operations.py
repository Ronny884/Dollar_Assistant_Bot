import sqlite3


class DataBaseClient:
    def __init__(self, filepath):
        self.filepath = filepath
        self.conn = None

    def create_conn(self):
        self.conn = sqlite3.connect(self.filepath, check_same_thread=False)

    def execute_command_with_params(self, command, params):
        if self.conn is not None:
            self.conn.execute(command, params)
            self.conn.commit()
        else:
            raise ConnectionError('Вы не подключены к базе данных')

    def execute_command_without_params(self, command):
        if self.conn is not None:
            self.conn.execute(command)
            self.conn.commit()
        else:
            raise ConnectionError('Вы не подключены к базе данных')

    def execute_select_command(self, command):
        if self.conn is not None:
            cur = self.conn.cursor()
            cur.execute(command)
            return cur.fetchall()
        else:
            raise ConnectionError('Вы не подключены к базе данных')

    def close_conn(self):
        self.conn.close()


class UserActioner:
    GET_USER = '''SELECT user_id, username, time_interval, delta, everyday_time FROM users WHERE user_id = %s'''

    SELECT_ALL_USERS_INFO = '''SELECT * FROM users'''

    CREATE_USER = '''INSERT INTO users(user_id, username, time_interval, delta, everyday_time) VALUES(?, ?, ?, ?, ?)'''

    CREATE_TABLE = '''CREATE TABLE IF NOT EXISTS users (
    user_id TEXT NOT NULL,
    username TEXT,
    time_interval TEXT,
    delta TEXT,
    everyday_time TEXT)
    '''

    UPDATE_TIME_INTERVAL = '''UPDATE users SET time_interval = ? WHERE user_id = ?'''
    UPDATE_DELTA = '''UPDATE users SET delta = ? WHERE user_id = ?'''
    UPDATE_EVERYDAY_TIME = '''UPDATE users SET everyday_time = ? WHERE user_id = ?'''

    def __init__(self, database_client):
        self.database_client = database_client

    def setup(self):
        self.database_client.create_conn()

    def create_table(self):
        self.database_client.execute_command_without_params(self.CREATE_TABLE)

    def get_user(self, user_id):
        user = self.database_client.execute_select_command(self.GET_USER % user_id)
        return user[0] if user else []

    def select_all_users_info(self):
        all_users_info = self.database_client.execute_select_command(self.SELECT_ALL_USERS_INFO)
        return all_users_info

    def create_user(self, user_id, username, time_interval, delta, everyday_time):
        self.database_client.execute_command_with_params(self.CREATE_USER, (user_id, username, time_interval,
                                                                            delta, everyday_time))

    def shutdown(self):
        self.database_client.close_conn()

    def update_time_interval(self, user_id, time_interval):
        self.database_client.execute_command_with_params(self.UPDATE_TIME_INTERVAL, (time_interval, user_id))

    def update_delta(self, user_id, delta):
        self.database_client.execute_command_with_params(self.UPDATE_DELTA, (delta, user_id))

    def update_everyday_time(self, user_id, everyday_time):
        self.database_client.execute_command_with_params(self.UPDATE_EVERYDAY_TIME, (everyday_time, user_id))








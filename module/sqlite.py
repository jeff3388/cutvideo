from beartype import beartype
import pandas as pd
import sqlite3
import datetime

def today_time():
    datetime_dt = datetime.datetime.today() # 獲得當地時間
    datetime_str = datetime_dt.strftime("%Y-%m-%d %H:%M:%S")  # 格式化日期
    return datetime_str

class sqlTool:

    def __init__(self):
        self.cur = None
        self.conn = None
        self.table_name = 'user_info'

    @beartype
    def open_connection(self):
        db_name = './manager.db'
        timeout = 30000
        conn = sqlite3.connect(db_name,
                               isolation_level=None,
                               check_same_thread=False,
                               timeout=timeout)

        cur = conn.cursor()

        # 確認 table 是否存在
        cur.execute(f'CREATE TABLE IF NOT EXISTS {self.table_name}'
                    f'(id INTEGER PRIMARY KEY AUTOINCREMENT, '
                    f'username TEXT, password TEXT, create_time TEXT)')
        conn.commit()

        self.cur = cur
        self.conn = conn

    @beartype
    def close_connection(self):

        self.cur.close()
        self.conn.close()

    @beartype
    def insert_data(self, username: str, password: str):

        self.open_connection()
        df = pd.DataFrame({'username': [username],
                           'password': [password],
                           'create_time': [today_time()]
                           })

        df.to_sql(self.table_name, self.conn, if_exists='append', index=False)
        self.close_connection()

    @beartype
    def insert_cookies(self, account: str, cookies: str):
        self.open_connection()
        sql = f'''INSERT INTO {self.table_name} 
                (account, cookies)
                VALUES ("{account}", "{cookies}")
                '''
        self.cur.execute(sql)
        self.conn.commit()
        self.close_connection()

    @beartype
    def update_cookies(self, account: str, cookies: str):
        self.open_connection()
        sql = f'''UPDATE {self.table_name} 
                     SET cookies = "{cookies}"
                     WHERE account = "{account}"
                     '''
        self.cur.execute(sql)
        self.conn.commit()

        self.close_connection()

    @beartype
    def select_cookies(self):
        sql = f'''
            SELECT * 
            FROM {self.table_name}
            '''

        self.open_connection()
        df = pd.read_sql(sql, self.conn)
        df_dict = df.to_dict('records')
        self.close_connection()

        return df_dict

    @beartype
    def select_user_info(self, username: str):

        sql = '''
        SELECT * 
        FROM {}
        WHERE `username` = "{}"
        LIMIT 1
        '''
        sql = sql.format(self.table_name, username)
        self.open_connection()

        df = pd.read_sql(sql, self.conn)
        df_dict = df.to_dict('records')

        self.close_connection()

        return df_dict

if __name__ == '__main__':
    username = 'jojobot'
    # username = ['jojobot']
    # password = ['123qwe']
    # create_time = [today_time()]
    DB = sqlTool()
    # result = DB.insert_data(username, password, create_time)
    result = DB.select_user_info(username)


    print(result)

import pymysql
from DBUtils.PersistentDB import PersistentDB


## MySQL 連線設定 ##
def db_config():
    db_dict = {
                'MySql_IP': '85.209.158.248',
                'MySql_Port': 3306,
                'MySql_account': 'root',
                'MySql_password': '12ds4@$#%fdsf',
                'MySql_db_name': 'crawler_article'
                }

    POOL = PersistentDB(
        creator=pymysql,
        maxusage=None,
        setsession=[],
        ping=0,
        closeable=False,
        threadlocal=None,
        host=db_dict['MySql_IP'],
        port=db_dict['MySql_Port'],
        user=db_dict['MySql_account'],
        password=db_dict['MySql_password'],
        database=db_dict['MySql_db_name'],
        charset='utf8'
    )

    return POOL


def select_data(POOL):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    SQL = '''
        SELECT *
        FROM article
        WHERE `state`= 0
        LIMIT 10
      '''
    try:
        with conn:
            cursor.execute(SQL)
            rows = cursor.fetchall()
            return rows
    except Exception as e:
        print(e)
        conn.rollback()


def update_data(POOL, Id=None):
    conn = POOL.connection(shareable=False)
    cursor = conn.cursor()
    SQL = '''
            UPDATE article
            SET `state` = 1
            WHERE `id`= (%s)
    '''

    # SQL = '''
    #             UPDATE article
    #             SET `state` = 0
    #             WHERE `state`= 1
    #     '''

    try:
        with conn:
            cursor.executemany(SQL, Id)
            # cursor.execute(SQL)
    except Exception as e:
        print(e)
        conn.rollback()

if __name__ == '__main__':
    Pool = db_config()
    update_data(Pool)
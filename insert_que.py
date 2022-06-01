from module.sqlite import sqlTool
import requests


def insert_que():
    url = 'http://127.0.0.1:5501/append_deque'
    db = sqlTool()
    result_ls = db.select_latest_article()
    if bool(result_ls) is True:
        for result in result_ls:
            title = result.get('title')
            content = result.get('content')
            md5_key = result.get('md5_key')
            db.update_article_state(state='1', md5_key=md5_key)

            data = {"title": title, "content": content}
            requests.post(url=url, json=data)

# db = sqlTool()
# db.update_all_article_state()

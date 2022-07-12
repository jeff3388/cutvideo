import requests
from bs4 import BeautifulSoup
from module.sqlite import sqlTool
import hashlib

headers = {

    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}

db = sqlTool()

def md5(string: str):
    md = hashlib.md5()
    md.update(string.encode('utf-8'))

    return md.hexdigest()

def fetch_article_link():
    total_link = []
    for i in range(1, 3):
        url = f'https://twseo.com.tw/page/{str(i)}'
        res = requests.get(url=url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'lxml')
        ele_ls = soup.find_all('h2', attrs={
            "class": "alignwide wp-block-post-title has-var-wp-custom-typography-font-size-huge-clamp-2-25-rem-4-vw-2-75-rem-font-size"})

        total_link += [[ele.find('a').get('href') for ele in ele_ls]]

    return sum(total_link, [])


def main(table_name):
    total_url = fetch_article_link()

    total_dict_ls = []
    for url in total_url:
        res = requests.get(url=url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'lxml')
        art_title = soup.find('h1', attrs={'class': 'alignwide wp-block-post-title'}).text
        art_content = soup.find('div', attrs={'class': 'wp-container-7 entry-content wp-block-post-content'}).text
        total_dict_ls += [{'title': art_title, 'content': art_content}]

    for article in total_dict_ls:
        title = article.get('title')
        content = article.get('content')
        md_key = md5(title + content)
        result = db.crawler_select_article(table_name, md_key)
        if bool(result) is False:
            db.insert_article(table_name, title, content)

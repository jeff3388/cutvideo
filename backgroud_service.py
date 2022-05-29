from flask import Flask, render_template, flash
from flask import request, session, redirect, url_for
from datetime import timedelta
from module.sqlite import sqlTool
import os

db = sqlTool()
app = Flask(__name__)

# session 存活時間
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=10)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')

        # 更新 session
        session['username'] = username

        # 驗證帳號是否存在
        result = db.select_user_info(username)
        if bool(result) is False:
            err = '帳號不存在'
            return render_template('login_error.html', err=err)

        elif bool(result) is True:
            db_password = result.pop().get('password')
            if password != db_password:
                err = '帳號密碼錯誤'
                return render_template('login_error.html', err=err)

        return redirect(url_for('article'))
    else:
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        render_template('login.html')
    else:
        return redirect(url_for('login'))


@app.route('/')
@app.route('/404')
def not_found():
    return render_template('404.html')


@app.route('/article', methods=['GET', 'POST'])
def article():
    if 'username' in session:
        if request.method == 'POST':
            title = request.values.get('title')
            content = request.values.get('text_area')
            db.insert_article(title, content)

            return render_template('article.html')
        else:
            return render_template('article.html')
    else:
        return render_template('login.html')

@app.route('/article_list', methods=['GET', 'POST'])
def article_list():
    if 'username' in session:

        content_ls = []
        result_ls = db.select_latest_article()
        for result in result_ls:
            title = result.get('title')
            content = result.get('content')

            content_ls += [{'title': title, 'content': content}]

        return render_template('article_list.html', content_ls=content_ls)
    else:
        return redirect(url_for('login'))


@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if all(['username' in session, request.method == 'GET']):
        return render_template('add_account.html')

    if all(['username' in session, request.method == 'POST']):
        username = request.values.get('username')
        password = request.values.get('password')

        result = db.select_user_info(username)
        if bool(result) is False:
            db.insert_user_info(username, password)
            return render_template('add_account.html', result='創建成功')
        else:
            return render_template('add_account.html', result='帳號已存在')

    else:
        return redirect(url_for('login'))


@app.route('/status', methods=['GET', 'POST'])
def status():
    if 'username' in session:
        # 從 DB 獲取文章狀態
        done_quantity = "1"
        pending_quantity = "39"

        return render_template('article.html', done_quantity=done_quantity, pending_quantity=pending_quantity)
    else:
        return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)
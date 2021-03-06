from flask import Flask, render_template, jsonify
from flask import request, redirect, url_for
from module.decorator_method import validate_json
from datetime import timedelta
from module.sqlite import sqlTool
import json
import os

db = sqlTool()
app = Flask(__name__)

# session 存活時間
# app.config['SECRET_KEY'] = os.urandom(24)
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=10)

admit_ls = []

success_alert_content = """    
  <div style="text-align:center; color:green ;">
    <h3>創建成功</h3>
    </div>
"""

fail_alert_content = """
  <div style="text-align:center; color:red ;">
    <h3>創建失敗</h3>
    </div>
"""


article_ls = """
<div class="card shadow mb-4" style="width:800px">
        <!-- Card Header - Accordion -->
        <a href="#collapseCardExample" class="d-block card-header py-3" data-toggle="collapse" data-target="#collapse{}"
            role="button" aria-expanded="true" aria-controls="collapseCardExample">
            <h6 class="m-0 font-weight-bold text-primary">{}</h6>
        </a>
        <!-- Card Content - Collapse -->
        <div class="collapse show" id="collapse{}">
            <div class="card-body">
                {}
            </div>
        </div>
</div>
"""


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')

        if username == 'jojo':
            return render_template('article.html')

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

        # 最高管理權限顯示此頁面
        elif username in admit_ls:
            return render_template('admit_article.html')

        return redirect(url_for('article_client'))

    elif request.method == 'GET':
        return render_template('login.html')


@app.route('/article_client', methods=['GET'])
def article_client():
    return render_template('article_client.html')


@app.route('/logout', methods=['GET'])
def logout():
    return redirect(url_for('login'))


@app.route('/')
@app.route('/index')
def index():
    return render_template('login.html')


@app.route('/article', methods=['GET', 'POST'])
def article():

    if request.method == 'POST':
        title = request.values.get('title')
        content = request.values.get('text_area')
        table_name = request.values.get('table_name')
        db.insert_article(table_name, title, content)

        return render_template('article.html')
    else:
        return render_template('article.html')



@app.route('/article_list', methods=['GET', 'POST'])
def article_list():
    content_ls = []
    if request.method == 'POST':
        table_name = request.values.get('table_name')
        result_ls = db.select_latest_article(table_name)
        for i, result in enumerate(result_ls):
            title = result.get('title')
            content = result.get('content')

            article_html_ls = article_ls.format(str(i), title, str(i), content)
            content_ls += [article_html_ls]

    return render_template('article_list.html', article_list="\n".join(content_ls))


@app.route('/table', methods=['GET', 'POST'])
def table():
    return render_template('table.html')


@app.route('/add_account', methods=['GET', 'POST'])
def add_account():
    if request.method == 'GET':
        return render_template('add_account.html')

    if request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')

        result = db.select_user_info(username)
        if bool(result) is False:
            db.insert_user_info(username, password)
            return render_template('add_account.html', result=success_alert_content)
        else:
            return render_template('add_account.html', result=fail_alert_content)

    else:
        return redirect(url_for('login'))


@app.route('/submit_article', methods=['POST'])
def submit_article():
    if request.method == 'POST':
        table_name = request.values.get('tableName')
        title = request.values.get('title')
        content = request.values.get('content')
        db.insert_article(table_name, title, content)

        return redirect(url_for('article_client'))


@app.route('/status', methods=['GET', 'POST'])
def status():

    # 從 DB 獲取文章狀態
    done_quantity = "1"
    pending_quantity = "39"

    return render_template('article.html', done_quantity=done_quantity, pending_quantity=pending_quantity)


@app.route('/update_all_article_state', methods=['POST'])
@validate_json('auth', 'table_name')
def update_all_article_state():
    auth = request.json.get('auth')
    if auth != '7b354b2f9429e2b92ca5b8c0d12e22ef':
        return jsonify({"result": "abort your request"})

    table_name = request.json.get('table_name')
    db.update_all_article_state(table_name)

    return jsonify({"result": "already reset all article"})


@app.route('/add_table', methods=['GET'])
def add_table():
    return render_template('add_table.html')

@app.route('/background_create_table', methods=['GET', 'POST'])
def background_create_table():
    if request.method == 'GET':
        return render_template('add_table.html')
    elif request.method == 'POST':
        token = request.json.get('token')
        tableName = request.json.get('tableName')
        if token != 'jojo':
            return redirect(url_for('login'))
        else:
            db.create_table(tableName)
            return render_template('add_table.html')


@app.route('/create_table', methods=['POST'])
@validate_json('auth')
def create_table():
    auth = request.json.get('auth')
    if auth != '7b354b2f9429e2b92ca5b8c0d12e22ef':
        return jsonify({"result": "abort your request"})

    table_name = request.json.get('table_name')
    db.create_table(table_name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

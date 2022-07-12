from flask import Flask, render_template, jsonify
from flask import request, session, redirect, url_for
from module.decorator_method import validate_json
from datetime import timedelta
from module.sqlite import sqlTool
import os

db = sqlTool()
app = Flask(__name__)

# session 存活時間
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=10)

admit_ls = []

success_alert_content = """    
  <div style="text-align:center; color:green ;">
    <h3>文章提交成功</h3>
    </div>
"""

fail_alert_content = """
  <div style="text-align:center; color:red ;">
    <h3>創建失敗</h3>
    </div>
"""

alert_content = """
  <div style="text-align:center; color:red ;">
    <h3>表單不得為空值</h3>
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
@app.route('/')
@app.route('/submit_article', methods=['GET', 'POST'])
def submit_article():
    if request.method == 'POST':
        table_name = request.values.get('table_name')
        title = request.values.get('title')
        content = request.values.get('content')

        if any([table_name != '', title != '', content != '']):
            return render_template('article_client.html', result=alert_content)

        db.insert_article(table_name, title, content)
        return render_template('article_client.html', result=success_alert_content)

    return render_template('article_client.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)

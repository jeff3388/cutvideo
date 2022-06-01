from flask import request, jsonify, Flask
from module.decorator_method import validate_json
from module.sqlite import sqlTool

db = sqlTool()
app = Flask(__name__)


@validate_json('auth')
@app.route('/article_list_json', methods='POST')
def article_list_json():
    auth = request.json.get('auth')
    if auth != '7b354b2f9429e2b92ca5b8c0d12e22ef':
        return jsonify({"result": "abort your request"})

    article_ls = []

    result_ls = db.select_latest_article()
    for result in result_ls:
        title = result.get('title')
        content = result.get('content')
        article_ls += [{"title": title, "content": content}]

    return jsonify({"result": article_ls})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5501)
from flask import request, jsonify, Flask
from module.decorator_method import validate_json

from collections import deque

q = deque()
app = Flask(__name__)


@app.route('/append_deque', methods=['POST'])
def append_deque():
    title = request.json.get('title')
    content = request.json.get('content')
    q.append({'title': title, 'content': content})

    return jsonify({"result": "1"})


@app.route('/article_list_json', methods=['POST'])
@validate_json('auth')
def article_list_json():
    auth = request.json.get('auth')
    if auth != '7b354b2f9429e2b92ca5b8c0d12e22ef':
        return jsonify({"result": "abort your request"})

    if len(q):
        result = q.pop()
    else:
        result = {}

    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5501)
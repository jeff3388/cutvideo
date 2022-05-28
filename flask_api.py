from flask import Flask, request, jsonify
from decorator_method import validate_json, error_handle
from flask import make_response
from mysql_tool import select_data, db_config, update_data

app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/fetch_article', methods=['POST'])
@validate_json('auth_key')
@error_handle
def fetch_article():

    auth_key = request.json.get('auth_key')
    if auth_key != 'jojo!~#$bot':
        return jsonify({"result": "reject your request", "s": "-1"})

    Pool = db_config()
    data = list(select_data(Pool))

    Id_ls = list(map(lambda x: (x[0]), data))
    title_ls = list(map(lambda x: x[1], data))
    content_ls = list(map(lambda x: x[2], data))

    result_json = [{'title': title, 'content': content} for title, content in zip(title_ls, content_ls)]

    update_data(Pool, Id_ls)

    return jsonify({"result": result_json, "s": "1"})


if __name__ == '__main__':
    host = '0.0.0.0'
    port = 9453
    debug = True
    app.run(host=host, port=port, debug=debug)

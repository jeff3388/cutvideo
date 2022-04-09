from flask import abort, Response, jsonify, request
from functools import wraps
import functools

# verify post data json key
def validate_json(*default_args):
    def decorator_validate_json(function_name):

        @wraps(function_name)
        def wrapper(*args):
            if not request.get_json():
                abort(Response('request must be json format'))

            json_object = request.get_json()
            for default_arg in default_args:
                if default_arg not in json_object:
                    abort(Response('You are missing this json key: {}'.format(str(default_arg))))

            return function_name(*args)

        return wrapper

    return decorator_validate_json


def error_handle(func):
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError as v:
            return jsonify({"error": str(v), "s": "-1"})

        except Exception as e:
            return jsonify({"error": str(e), "s": "-1"})

    return functools.update_wrapper(wrapper_func, func)

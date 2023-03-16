#!/usr/bin/env python3
"""
    flask app
"""
from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """
        returns JSON payload
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users() -> str:
    """
        end-point to register a user
        return: JSON payload
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
        end point to login a user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or password is None:
        abort(401)
    if AUTH.valid_login(email, password):
        sessionID = AUTH.create_session(email)
        resp = make_response(jsonify({"email": email, "message": "logged in"}))
        resp.set_cookie('session_id', sessionID)
        return resp
    else:
        abort(401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
